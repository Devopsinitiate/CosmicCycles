from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import user_cycle_api
from .models import UserProfile, Business
import datetime
import json

class UserCycleIntegrationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='inttest', password='pass')
        # ensure profile exists
        up, _ = UserProfile.objects.get_or_create(user=self.user)
        up.date_of_birth = datetime.date(1990,1,1)
        up.save()

    def test_human_cycle_generic_endpoint(self):
        request = self.factory.get('/api/user_cycle/human/')
        request.user = self.user
        response = user_cycle_api(request, 'human')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('periods', data)
        self.assertIn('template', data)

    def test_daily_cycle_generic_endpoint(self):
        request = self.factory.get('/api/user_cycle/daily/')
        request.user = self.user
        response = user_cycle_api(request, 'daily')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('periods', data)

    def test_unauthenticated_redirects(self):
        request = self.factory.get('/api/user_cycle/human/')
        # anonymous user
        request.user = User()
        response = user_cycle_api(request, 'human')
        # login_required decorator will return 302 redirect in this context
        self.assertIn(response.status_code, (302, 400))

    def test_dashboard_contains_data_progress_attrs(self):
        # login and fetch dashboard HTML, ensure data-progress attributes are present
        logged = self.client.login(username='inttest', password='pass')
        self.assertTrue(logged)
        # create a business to ensure business section renders
        Business.objects.create(user=self.user, name='BizA', establishment_date=datetime.date(2020,1,1))
        resp = self.client.get('/dashboard/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        # Check specific expected data-progress spots: human, yearly, soul and a business card
        self.assertIn('data-progress="', content)
        self.assertIn('id="soulProgressCircle"', content)
        self.assertIn('id="soulProgressText"', content)
        # human progress (bar inside human summary) should include data-progress
        self.assertIn('data-progress="', content)

    def test_business_api_single_business(self):
        # create a business and query the API for a single business
        biz = Business.objects.create(user=self.user, name='BizAPI', establishment_date=datetime.date(2020,1,1))
        request = self.factory.get(f'/api/user_cycle/business/?business_id={biz.id}')
        request.user = self.user
        response = user_cycle_api(request, 'business')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('business', data)
        b = data['business']
        # payload should contain fields for business preview
        self.assertIn('business', b)
        self.assertEqual(b['business'], biz.name)
        self.assertIn('progress', b)

    def test_user_cycle_api_returns_flattened_template(self):
        # Query the API first to learn the current period number, then create a CycleTemplate for that period
        request = self.factory.get('/api/user_cycle/human/')
        request.user = self.user
        response = user_cycle_api(request, 'human')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # determine current period number (fallback to 1)
        current_num = data.get('current_period_number') or 1
        from .models import CycleTemplate
        CycleTemplate.objects.create(
            cycle_type='human',
            period_number=current_num,
            description='Test desc',
            effects={'start_age': 0, 'end_age': 7, 'advice': 'do X', 'summary': 's'}
        )
        # re-request API and assert flattened template is now present
        request2 = self.factory.get('/api/user_cycle/human/')
        request2.user = self.user
        response2 = user_cycle_api(request2, 'human')
        self.assertEqual(response2.status_code, 200)
        data2 = json.loads(response2.content)
        self.assertIn('template', data2)
        tpl = data2['template']
        self.assertIsNotNone(tpl)
        # flattened keys should be present
        self.assertIn('description', tpl)
        self.assertIn('effects', tpl)
        self.assertIn('advice', tpl)
