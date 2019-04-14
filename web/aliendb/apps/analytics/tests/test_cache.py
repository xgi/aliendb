from django.test import TestCase, Client
from django.test.utils import override_settings
from django.core.cache import cache
from .common.db import create_dummy_models


@override_settings(DEBUG=False)
class CacheTest(TestCase):
    def setUp(self):
        self.client = Client()
        create_dummy_models()
        cache.clear()

    def test_cache_home(self):
        response = self.client.get('/')
        cached = cache.get("home_response")
        self.assertEqual(response.content, cached.content)

    def test_cache_subreddits(self):
        response = self.client.get('/subreddits')
        cached = cache.get("subreddits_response")
        self.assertEqual(response.content, cached.content)

    def test_cache_submission(self):
        response = self.client.get('/submission/000001')
        cached = cache.get("submission_response_000001")
        self.assertEqual(response.content, cached.content)

    def test_cache_subreddit(self):
        response = self.client.get('/r/testsubreddit')
        cached = cache.get("subreddit_response_testsubreddit")
        self.assertEqual(response.content, cached.content)
