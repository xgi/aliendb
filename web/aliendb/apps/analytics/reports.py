from django.core.cache import cache

from .models import *
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def submission(request):
    id = request.GET.get('id', '')

    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission was not found")

    # try to get full data variable from cache
    data = cache.get("submission_data_%s" % id)
    if data is not None:
        return data

    comments = Comment.objects.filter(submission=submission)
    submission_scores = SubmissionScore.objects.filter(submission=submission).order_by('timestamp')
    submission_num_comments = SubmissionNumComments.objects.filter(submission=submission).order_by('timestamp')
    submission_upvote_ratios = SubmissionUpvoteRatio.objects.filter(submission=submission).order_by('timestamp')

    # try to get some variables from cache
    subreddit_submissions = cache.get("subreddit_submissions_%s" % submission.subreddit)
    subreddit_comments = cache.get("subreddit_comments_%s" % submission.subreddit)

    # check if they weren't found in cache
    if subreddit_submissions is None:
        subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)
        cache.set("subreddit_submissions_%s" % submission.subreddit, subreddit_submissions, 600)
    if subreddit_comments is None:
        subreddit_comments = [c for queryset in [Comment.objects.filter(submission_id=s.id) for s in subreddit_submissions] for c in queryset]
        cache.set("subreddit_comments_%s" % submission.subreddit, subreddit_comments, 600)

    ## activity
    score_tallies = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.score] for s in submission_scores]
    comment_tallies = [[int((c.timestamp - epoch).total_seconds()) * 1000.0, c.num_comments] for c in submission_num_comments]

    ## upvote_ratio
    upvote_ratios = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.upvote_ratio] for s in submission_upvote_ratios]

    # get average ratio for subreddit
    total_upvote_ratio = 0
    for submission in subreddit_submissions:
        total_upvote_ratio += submission.upvote_ratio
    average_upvote_ratio = total_upvote_ratio / len(subreddit_submissions)
    average_upvote_ratio = float("{0:.2f}".format(average_upvote_ratio))

    ## special_users
    special_users_submission = [
        [c.is_op for c in comments].count(True),
        [c.is_mod for c in comments].count(True),
        [c.is_admin for c in comments].count(True),
        [c.is_special for c in comments].count(True)
    ]
    special_users_subreddit = [
        [c.is_op for c in comments].count(True) / len(subreddit_submissions),
        [c.is_mod for c in comments].count(True) / len(subreddit_submissions),
        [c.is_admin for c in comments].count(True) / len(subreddit_submissions),
        [c.is_special for c in comments].count(True) / len(subreddit_submissions)
    ]

    ## gilded
    gilded_submission = sum(c.gilded for c in comments)
    gilded_subreddit = sum(c.gilded for c in subreddit_comments) / len(subreddit_submissions)

    ## polarity
    polarity_submission = [
        submission.polarity,
        sum(c.polarity for c in comments) / len(comments)
    ]
    polarity_subreddit = [
        sum(s.polarity for s in subreddit_submissions) / len(subreddit_submissions),
        sum(c.polarity for c in subreddit_comments) / len(subreddit_comments)
    ]

    ## subjectivity
    subjectivity_submission = [
        submission.subjectivity,
        sum(c.subjectivity for c in comments) / len(comments)
    ]
    subjectivity_subreddit = [
        sum(s.subjectivity for s in subreddit_submissions) / len(subreddit_submissions),
        sum(c.subjectivity for c in subreddit_comments) / len(subreddit_comments)
    ]

    data = {
        'activity': {
            'scores': score_tallies,
            'comments': comment_tallies
        },
        'upvote_ratio': {
            'upvote_ratios': upvote_ratios,
            'average_upvote_ratio': average_upvote_ratio
        },
        'special_users': {
            'submission': special_users_submission,
            'subreddit': special_users_subreddit
        },
        'gilded': {
            'data': [
                gilded_submission,
                gilded_subreddit
            ]
        },
        'polarity': {
            'submission': polarity_submission,
            'subreddit': polarity_subreddit
        },
        'subjectivity': {
            'submission': subjectivity_submission,
            'subreddit': subjectivity_subreddit
        }
    }

    cache.set("submission_data_%s" % id, data, 600)

    return data
