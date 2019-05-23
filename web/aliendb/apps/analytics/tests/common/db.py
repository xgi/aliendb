from ...models import *
from ...views import *
import datetime


def create_dummy_models():
    subreddit = Subreddit.objects.create(
        name="testsubreddit",
        title="testsubreddit title",
        description="testsubreddit description"
    )
    subreddit2 = Subreddit.objects.create(
        name="emptysubreddit",
        title="emptysubreddit title",
        description="emptysubreddit description"
    )
    submission = Submission.objects.create(
        id="000001",
        subreddit=subreddit,
        title="mytitle",
        author="myauthor",
        rank=1,
        rank_previous=2,
        rank_peak=1,
        score=10000,
        num_comments=200,
        num_sample_comments=0,
        polarity=-0.50,
        subjectivity=0.25,
        domain="i.redd.it",
        link_flair_text="myflair",
        upvote_ratio=0.95,
        stickied=True,
        over_18=False,
        spoiler=True,
        locked=False,
        gilded_silver=1,
        gilded_gold=2,
        gilded_platinum=3,
        comments_gilded_silver=0,
        comments_gilded_gold=0,
        comments_gilded_platinum=0,
        comments_root=0,
        comments_op=0,
        comments_mod=0,
        comments_admin=0,
        comments_special=0,
        comments_polarity=0,
        comments_subjectivity=0,
        created_at=datetime.datetime(2017, 10, 11, 12, 13, 14))
    score = SubmissionScore.objects.create(
        submission=submission,
        score=submission.score)
    num_comments = SubmissionNumComments.objects.create(
        submission=submission,
        num_comments=submission.num_comments)
    upvote_ratio = SubmissionUpvoteRatio.objects.create(
        submission=submission,
        upvote_ratio=submission.upvote_ratio)
