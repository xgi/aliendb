from django.test import TestCase
from ..models import Submission
from ..tasks import *
from .common.db import create_dummy_models
import pickle


class TasksTest(TestCase):
    def setUp(self):
        self.my_dir = os.path.dirname(os.path.realpath(__file__))

    def test_create_submission_obj(self):
        submission_id = '8djsdf'
        with open(self.my_dir + '/data/submission_%s.pk1' % submission_id, 'rb') as obj_file:
            submission = pickle.load(obj_file)
        create_submission_obj(submission, 1)
        assert Submission.objects.filter(id=submission_id).exists()

    def test_update_submission_obj(self):
        submission_id = '8djsdf'
        with open(self.my_dir + '/data/submission_%s.pk1' % submission_id, 'rb') as obj_file:
            submission = pickle.load(obj_file)
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

    def test_create_submission_tracker_objs(self):
        submission_id = '8djsdf'
        with open(self.my_dir + '/data/submission_%s.pk1' % submission_id, 'rb') as obj_file:
            submission = pickle.load(obj_file)
        submission_obj = create_submission_obj(submission, 1)
        create_submission_tracker_objs(submission_obj, submission)
        assert SubmissionScore.objects.filter(
            submission=submission_obj).exists()
        assert SubmissionNumComments.objects.filter(
            submission=submission_obj).exists()
        assert SubmissionUpvoteRatio.objects.filter(
            submission=submission_obj).exists()

    def test_create_cumulative_tracker_objs(self):
        submission_id = '8djsdf'
        with open(self.my_dir + '/data/submission_%s.pk1' % submission_id, 'rb') as obj_file:
            submission = pickle.load(obj_file)
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
