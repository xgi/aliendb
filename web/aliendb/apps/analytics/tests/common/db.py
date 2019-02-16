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
        created_at=datetime.datetime(2017, 10, 11, 12, 13, 14))
    comment = Comment.objects.create(
        id="000002",
        submission=submission,
        score=500,
        is_root=True,
        is_op=True,
        is_mod=False,
        is_admin=False,
        is_special=False,
        gilded_silver=4,
        gilded_gold=5,
        gilded_platinum=6,
        characters=50,
        words=10,
        sentences=2,
        polarity=-0.75,
        subjectivity=0.50,
        created_at=datetime.datetime(2017, 10, 11, 15, 16, 17))
    score = SubmissionScore.objects.create(
        submission=submission,
        score=submission.score)
    num_comments = SubmissionNumComments.objects.create(
        submission=submission,
        num_comments=submission.num_comments)
    upvote_ratio = SubmissionUpvoteRatio.objects.create(
        submission=submission,
        upvote_ratio=submission.upvote_ratio)
