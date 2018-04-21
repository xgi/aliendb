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
        response = self.client.get('/api?name=submission&id=000001')
        self.assertEqual(response.status_code, 200)

    def test_api_submission_404(self):
        response = self.client.get('/api?name=submission&id=222222')
        self.assertEqual(response.status_code, 404)

    def test_api_subreddit_200(self):
        response = self.client.get('/api?name=subreddit&id=testsubreddit')
        self.assertEqual(response.status_code, 200)

    def test_api_subreddit_404(self):
        response = self.client.get('/api?name=subreddit&id=notarealsubreddit')
        self.assertEqual(response.status_code, 404)

    def test_api_cumulative_200(self):
        response = self.client.get('/api?name=cumulative&timerange=day')
        self.assertEqual(response.status_code, 200)
