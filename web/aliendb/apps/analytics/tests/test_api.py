from django.test import TestCase, Client
from django.test.utils import override_settings
from .common.db import create_dummy_models


class APITest(TestCase):
    # TODO: Add more methods to test returned API values. Will likely require a
    # more elaborate data set to test from. Maybe freeze a copy of the database
    # to use for this kind of testing?
    def setUp(self):
        self.client = Client()
        create_dummy_models()

    def test_api_submission_200(self):
        # run twice to hit the cache
        response1 = self.client.get('/api?name=submission&id=000001')
        response2 = self.client.get('/api?name=submission&id=000001')
        assert response1.content == response2.content
        self.assertEqual(response1.status_code, 200)

    def test_api_submission_404(self):
        response = self.client.get('/api?name=submission&id=222222')
        self.assertEqual(response.status_code, 404)

    def test_api_subreddit_200(self):
        # run twice to hit the cache
        response1 = self.client.get('/api?name=subreddit&id=testsubreddit')
        response2 = self.client.get('/api?name=subreddit&id=testsubreddit')
        assert response1.content == response2.content
        self.assertEqual(response1.status_code, 200)

    def test_api_subreddit_404(self):
        response = self.client.get('/api?name=subreddit&id=notarealsubreddit')
        self.assertEqual(response.status_code, 404)

    def test_api_cumulative_200(self):
        timeranges = ['day', 'week', 'fortnight', 'month', 'year']
        for timerange in timeranges:
            response = self.client.get(
                '/api?name=cumulative&timerange=%s' % timerange
            )
            self.assertEqual(response.status_code, 200)
