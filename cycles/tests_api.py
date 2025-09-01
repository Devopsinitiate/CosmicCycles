import json
import datetime
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from cycles.models import UserProfile
from cycles.views import human_cycle_api


class HumanCycleAPITest(TestCase):
    def setUp(self):
        self.username = 'apitest'
        self.password = 'testpass'
        self.email = 'api@test.com'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        # Ensure a single UserProfile exists
        UserProfile.objects.get_or_create(user=self.user)

    def test_missing_birth_date_returns_400(self):
        factory = RequestFactory()
        request = factory.get('/api/user_cycle/human/')
        request.user = self.user
        response = human_cycle_api(request)
        self.assertEqual(response.status_code, 400)
        payload = json.loads(response.content.decode())
        self.assertEqual(payload.get('error'), 'birth_date_missing')

    def test_with_birth_date_returns_200_and_structure(self):
        up = self.user.userprofile
        up.date_of_birth = datetime.date(1990, 1, 1)
        up.save()
        factory = RequestFactory()
        request = factory.get('/api/user_cycle/human/')
        request.user = self.user
        response = human_cycle_api(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertIn('periods', data)
        self.assertIn('current_period', data)
        self.assertIn('progress', data)
        self.assertIsInstance(data['periods'], list)

    def test_unauthenticated_redirects_to_login(self):
        # When no user is authenticated, login_required should redirect to login page
        from django.contrib.auth.models import AnonymousUser
        factory = RequestFactory()
        request = factory.get('/api/user_cycle/human/')
        request.user = AnonymousUser()
        response = human_cycle_api(request)
        # login_required decorator returns a HttpResponseRedirect to login URL
        self.assertTrue(hasattr(response, 'status_code'))
        self.assertIn(response.status_code, (302, 401, 403))
