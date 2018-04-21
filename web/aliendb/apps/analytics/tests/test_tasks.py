from django.test import TestCase
from ..models import Submission
from ..tasks import *
from .common.db import create_dummy_models
import vcr


class TasksTest(TestCase):
    def test_create_submission_obj(self):
        submission_id = '4vx5ko'
        with vcr.use_cassette('cassettes/submission1.yaml'):
            submission = reddit.submission(id=submission_id)
            submission.score
        create_submission_obj(submission, 1)
        assert Submission.objects.filter(id=submission_id).exists()

    def test_update_submission_obj(self):
        submission_id = '4vx5ko'
        with vcr.use_cassette('cassettes/submission1.yaml'):
            submission = reddit.submission(id=submission_id)
            submission.score
        submission_obj = create_submission_obj(submission, 1)

        new_score = 51
        new_num_comments = 52
        new_rank = 2
        submission.score = new_score
        submission.num_comments = new_num_comments

        assert submission_obj.score != new_score
        assert submission_obj.num_comments != new_num_comments
        assert submission_obj.rank != new_rank
        submission_obj = update_submission_obj(submission, new_rank)
        assert submission_obj.score == new_score
        assert submission_obj.num_comments == new_num_comments
        assert submission_obj.rank == new_rank

    def test_create_comment_obj(self):
        create_dummy_models()
        comment_id = 'dnz8azn'
        with vcr.use_cassette('cassettes/comment1.yaml'):
            comment = reddit.comment(id=comment_id)
            comment.score
        submission_obj = Submission.objects.get(id='000001')
        create_comment_obj(comment, submission_obj)
        assert Comment.objects.filter(id=comment_id).exists()

    def test_create_submission_tracker_objs(self):
        submission_id = '4vx5ko'
        with vcr.use_cassette('cassettes/submission1.yaml'):
            submission = reddit.submission(id=submission_id)
            submission.score
        submission_obj = create_submission_obj(submission, 1)
        create_submission_tracker_objs(submission_obj, submission)
        assert SubmissionScore.objects.filter(
            submission=submission_obj).exists()
        assert SubmissionNumComments.objects.filter(
            submission=submission_obj).exists()
        assert SubmissionUpvoteRatio.objects.filter(
            submission=submission_obj).exists()

    def test_create_cumulative_tracker_objs(self):
        submission_id = '4vx5ko'
        with vcr.use_cassette('cassettes/submission1.yaml'):
            submission = reddit.submission(id=submission_id)
            submission.score
        submission_obj = create_submission_obj(submission, 1)
        create_cumulative_tracker_objs(submission_obj)
        assert TotalScore.objects.filter(score=submission_obj.score).exists()
        assert TotalNumComments.objects.filter(
            num_comments=submission_obj.num_comments).exists()

    def test_create_subreddit_tracker_objs(self):
        create_dummy_models()
        subreddit = Subreddit.objects.get(name="testsubreddit")
        create_subreddit_tracker_objs(subreddit)
        assert SubredditScore.objects.filter(subreddit=subreddit).exists()
        assert SubredditNumComments.objects.filter(
            subreddit=subreddit).exists()
