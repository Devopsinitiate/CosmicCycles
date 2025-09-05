from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Business
import json


User = get_user_model()


class CycleApiExtraTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='pass')
        # create a profile via signal or directly
        self.client.login(username='tester', password='pass')

        # create a business for the user (include required establishment_date)
        import datetime
        self.business = Business.objects.create(user=self.user, name='Acme LLC', establishment_date=datetime.date(2020,1,1))

    def test_business_api_single_returns_business_cycles_array(self):
        url = reverse('user_cycle_api', args=['business'])
        resp = self.client.get(url + f'?business_id={self.business.id}')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('business_cycles', data)
        self.assertIsInstance(data['business_cycles'], list)
        self.assertGreaterEqual(len(data['business_cycles']), 1)
        item = data['business_cycles'][0]
        self.assertIn('business', item)
        self.assertIn('name', item['business'])
        self.assertIn('periods', item)
        self.assertIn('current_period', item)

    def test_soul_api_returns_periods_and_current(self):
        url = reverse('user_cycle_api', args=['soul'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertIn('periods', data)
        self.assertIsInstance(data['periods'], list)
        self.assertIn('current_period', data)
