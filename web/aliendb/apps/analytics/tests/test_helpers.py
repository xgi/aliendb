from django.test import TestCase
from ..helpers import *


class HelpersTest(TestCase):
    def test_update_average(self):
        average = 10
        value = 20
        tracked = 4
        new_average = update_average(average, value, tracked)
        self.assertEqual(new_average, 12)
    def test_timestamp_to_ms(self):
        date = datetime.datetime(2005, 6, 23)
        date_in_ms = timestamp_to_ms(date)
        self.assertEqual(date_in_ms, 1119484800000.0)