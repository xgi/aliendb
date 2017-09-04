from django.test import TestCase, Client
from .models import *
from .views import *
import datetime

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()                          
        subreddit = Subreddit.objects.create(name="testsubreddit", title="testsubreddit title",
                                             description="testsubreddit description")
        submission = Submission.objects.create(id="000001",
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
                                               created_at=datetime.datetime(2017, 10, 11, 12, 13, 14))
        comment = Comment.objects.create(id="000002",
                                         submission=submission,
                                         score=500,
                                         is_root=True,
                                         is_op=True,
                                         is_mod=False,
                                         is_admin=False,
                                         is_special=False,
                                         gilded=2,
                                         characters=50,
                                         words=10,
                                         sentences=2,
                                         polarity=-0.75,
                                         subjectivity=0.50,
                                         created_at=datetime.datetime(2017, 10, 11, 15, 16, 17))
        score = SubmissionScore.objects.create(submission=submission,
                                               score=submission.score)
        num_comments = SubmissionNumComments.objects.create(submission=submission,
                                                            num_comments=submission.num_comments)
        upvote_ratio = SubmissionUpvoteRatio.objects.create(submission=submission,
                                                            upvote_ratio=submission.upvote_ratio)

    def test_home_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    def test_subreddits_200(self):
        response = self.client.get('/subreddits')
        self.assertEqual(response.status_code, 200)
    def test_about_200(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
    def test_api_200(self):
        response = self.client.get('/api?name=submission&id=000001')
        self.assertEqual(response.status_code, 200)
    def test_submission_200(self):
        response = self.client.get('/submission/000001')
        self.assertEqual(response.status_code, 200)
    def test_subreddit_200(self):
        response = self.client.get('/subreddit/testsubreddit')
        self.assertEqual(response.status_code, 200)
    def test_search_200(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
    def test_search_match(self):
        response = self.client.get('/search?q=mytitle&order_by=karma&time=today&subreddits=testsubreddit')
        self.assertContains(response, "Found 1 match")