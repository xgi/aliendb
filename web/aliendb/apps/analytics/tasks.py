from celery import Celery
from django.conf import settings
import datetime
import math
import os
import praw, prawcore
import string
from textblob import TextBlob
from .models import Submission, SubmissionScore, SubmissionNumComments, SubmissionUpvoteRatio, Comment

app = Celery('tasks')
app.config_from_object('django.conf:settings')

r = praw.Reddit(client_id=os.environ['PRAW_CLIENT_ID'],
                client_secret=os.environ['PRAW_CLIENT_SECRET'],
                username=os.environ['PRAW_REDDIT_USERNAME'],
                password=os.environ['PRAW_REDDIT_PASSWORD'],
                user_agent=os.environ['PRAW_USER_AGENT'])

def create_comment_obj(comment, submission_obj):
    # creates comment model from praw comment

    # check if comment already exists in db
    if not Comment.objects.filter(id=comment.id).exists():
        # check if comment has been deleted
        if not hasattr(comment, 'body'):
            return

        # determine comment distinguised properties
        if comment.author is not None:
            is_op = comment.author.name==submission_obj.author
            if comment.distinguished:
                is_mod = 'moderator' in comment.distinguished
                is_admin = 'admin' in comment.distinguished
                is_special = 'special' in comment.distinguished
            else:
                is_mod = False
                is_admin = False
                is_special = False
        else:
            # author field is None, which means the user deleted their account
            is_op = None
            is_mod = None
            is_admin = None
            is_special = None

        # perform sentiment analysis on comment
        blob = TextBlob(comment.body)
        polarity = blob.polarity
        subjectivity = blob.subjectivity

        num_characters = sum(c in string.ascii_letters for c in comment.body)

        # determine complexity of comment with ARI
        # see: https://en.wikipedia.org/wiki/Automated_readability_index
        #if len(blob.words) > 0 and len(blob.sentences) > 0:
        #    num_characters = 0
        #    for word in blob.words:
        #        num_characters += len(word)
        #    ari = math.ceil(
        #        4.71 * (num_characters / len(blob.words)) +
        #        0.5 * (len(blob.words) / len(blob.sentences)) - 21.43)
        #else:
        #    ari = 0

        created_at = datetime.datetime.utcfromtimestamp(comment.created_utc)
        created_at = created_at.replace(tzinfo=datetime.timezone.utc)

        comment_obj = Comment(id=comment.id,
                              submission=submission_obj,
                              score=comment.score,
                              is_root=comment.is_root,
                              is_op=is_op,
                              is_mod=is_mod,
                              is_admin=is_admin,
                              is_special=is_special,
                              gilded=comment.gilded,
                              characters=num_characters,
                              words=len(blob.words),
                              sentences=len(blob.sentences),
                              polarity=polarity,
                              subjectivity=subjectivity,
                              created_at=created_at)
        comment_obj.save()

    else:
        # comment already exists in db
        comment_obj = Comment.objects.get(id=comment.id)
        comment_obj.score = comment.score
        comment_obj.gilded = comment.gilded
        comment_obj.save()

@app.task
def get_top_submissions():
    subreddit = r.subreddit('all')

    try:
        submissions = [submission for submission in subreddit.hot(limit=100)]
    except prawcore.exceptions.RequestException:
        # reddit api is likely unavailable
        return

    rank = 1
    submission_objs = []
    for submission in submissions:
        try:
            # Submission.objects.get() can raise Submission.DoesNotExist
            submission_obj = Submission.objects.get(id=submission.id)

            # determine rank on /r/all
            submission_obj.rank_previous = submission_obj.rank
            submission_obj.rank = rank
            if rank < submission_obj.rank_peak:
                submission_obj.rank_peak = rank
            # don't save this obj yet - ranks will be repeated
            submission_objs.append(submission_obj)

            # update Submission obj
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()

            # create new SubmissionScore object
            submission_score = SubmissionScore(submission=submission_obj,
                                               score=submission.score)
            submission_score.save()

            # create new SubmissionNumComments object
            submission_num_comments = SubmissionNumComments(submission=submission_obj,
                                                            num_comments=submission.num_comments)
            submission_num_comments.save()

            # create new SubmissionUpvoteRatio object
            submission_upvote_ratio = SubmissionUpvoteRatio(submission=submission_obj,
                                                            upvote_ratio=submission.upvote_ratio)
            submission_upvote_ratio.save()

            # update karma peak and comments peak if necessary
            if submission.score > submission_obj.karma_peak:
                submission_obj.karma_peak = submission.score
            if submission.num_comments > submission_obj.comments_peak:
                submission_obj.comments_peak = submission.num_comments

            # update submission details
            if submission.link_flair_text is not None:
                submission_obj.link_flair_text = submission.link_flair_text
            submission_obj.upvote_ratio = submission.upvote_ratio
            submission_obj.stickied = submission.stickied
            submission_obj.over_18 = submission.over_18
            submission_obj.spoiler = submission.spoiler
            submission_obj.locked = submission.locked

            # create new Comment objects if necessary
            if submission.num_comments > 500:
                # get the submission again, sorted by oldest comments
                submission = r.submission(id=submission.id)
                submission.comment_sort = 'old'
                submission.comments.replace_more(limit=0)
                # append new flattened comments to comments array
                comments += submission.comments.list()

            for comment in comments:
                create_comment_obj(comment, submission_obj)

        except Submission.DoesNotExist:
            # submission has not been added to db yet

            created_at = datetime.datetime.utcfromtimestamp(submission.created_utc)
            created_at = created_at.replace(tzinfo=datetime.timezone.utc)

            if hasattr(submission, 'author'):
                if submission.author is not None:
                    author = submission.author.name

            # perform sentiment analysis on submission title
            blob = TextBlob(submission.title)
            polarity = blob.polarity
            subjectivity = blob.subjectivity

            # create Submission object
            submission_obj = Submission(id=submission.id,
                                        title=submission.title,
                                        author=author or None,
                                        rank=rank,
                                        rank_previous=rank,
                                        rank_peak=rank,
                                        karma_peak=submission.score,
                                        comments_peak=submission.num_comments,
                                        subreddit=submission.subreddit,
                                        polarity=polarity,
                                        subjectivity=subjectivity,
                                        domain=submission.domain,
                                        link_flair_text=submission.link_flair_text or '',
                                        upvote_ratio=submission.upvote_ratio,
                                        stickied=submission.stickied,
                                        over_18=submission.over_18,
                                        spoiler=submission.spoiler,
                                        locked=submission.locked,
                                        created_at=created_at)
            submission_obj.save()

            # create SubmissionScore object
            submission_score = SubmissionScore(submission=submission_obj,
                                               score=submission.score)
            submission_score.save()

            # create SubmissionNumComments object
            submission_num_comments = SubmissionNumComments(submission=submission_obj,
                                                            num_comments=submission.num_comments)
            submission_num_comments.save()

            # create SubmissionUpvoteRatio object
            submission_upvote_ratio = SubmissionUpvoteRatio(submission=submission_obj,
                                                            upvote_ratio=submission.upvote_ratio)
            submission_upvote_ratio.save()

            # create Comment objects
            submission.comments.replace_more(limit=0)
            comments = submission.comments.list()

            if submission.num_comments > 500:
                # get the submission again, sorted by oldest comments
                submission.comment_sort = 'old'
                submission = r.submission(id=submission.id)
                submission.comments.replace_more(limit=0)
                # append new flattened comments to comments array
                comments += submission.comments.list()

            for comment in comments:
                create_comment_obj(comment, submission_obj)
        rank += 1

    # reset rank for submissions no longer in top 100
    submission_ids = [submission.id for submission in submissions]
    for submission_obj in Submission.objects.filter(rank__gt=0):
        if submission_obj.id not in submission_ids:
            submission_obj.rank = -1
            submission_obj.save()

    # save all submission db objects
    for submission_obj in submission_objs:
        submission_obj.save()
