from django.test import TestCase
from .utils import get_daily_cycle, get_yearly_cycle, get_business_cycle, get_soul_cycle, get_human_life_cycle
from datetime import datetime

class CycleUtilsTestCase(TestCase):
    def test_get_daily_cycle(self):
        periods, current_period = get_daily_cycle()
        self.assertEqual(len(periods), 7)
        self.assertIn(current_period, periods)

    def test_get_yearly_cycle(self):
        birth_date = datetime(1990, 1, 1).date()
        periods, current_period, progress = get_yearly_cycle(birth_date)
        self.assertEqual(len(periods), 7)
        self.assertIsNotNone(current_period)
        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 100)

    def test_get_business_cycle(self):
        establishment_date = datetime(2020, 1, 1).date()
        periods, current_period, progress = get_business_cycle(establishment_date)
        self.assertEqual(len(periods), 7)
        self.assertIsNotNone(current_period)
        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 100)

    def test_get_soul_cycle(self):
        periods, current_period, progress = get_soul_cycle()
        self.assertEqual(len(periods), 7)
        self.assertIsNotNone(current_period)
        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 100)

    def test_get_human_life_cycle(self):
        birth_date = datetime(1990, 1, 1).date()
        periods, current_period, progress = get_human_life_cycle(birth_date)
        self.assertEqual(len(periods), 20)  # 144 / 7 = 20 periods (approx)
        self.assertIsNotNone(current_period)
        self.assertGreaterEqual(progress, 0)
        self.assertLessEqual(progress, 100)
