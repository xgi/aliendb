from django.test import TestCase, Client
from django.test.utils import override_settings
from .common.db import create_dummy_models


@override_settings(DEBUG=True)
class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        create_dummy_models()

    def test_home_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_subreddits_200(self):
        response = self.client.get('/subreddits')
        self.assertEqual(response.status_code, 200)

    def test_about_200(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_submission_200(self):
        response = self.client.get('/submission/000001')
        self.assertEqual(response.status_code, 200)

    def test_submission_404(self):
        response = self.client.get('/submission/222222')
        self.assertEqual(response.status_code, 404)

    def test_subreddit_200(self):
        response = self.client.get('/r/testsubreddit')
        self.assertEqual(response.status_code, 200)

    def test_subreddit_404(self):
        response = self.client.get('/r/notarealsubreddit')
        self.assertEqual(response.status_code, 404)

    def test_empty_subreddit_404(self):
        response = self.client.get('/r/emptysubreddit')
        self.assertEqual(response.status_code, 404)

    def test_search_200(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)

    def test_search_match(self):
        response = self.client.get(
            '/search?q=mytitle&order_by=karma&time=all&subreddits=testsubreddit')
        self.assertContains(response, "Found 1 match")
