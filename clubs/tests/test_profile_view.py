from django.test import TestCase, TransactionTestCase
from clubs.models import User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next

class ProfileViewTestCase(TransactionTestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']
    def setUp(self):
        self.user = User.objects.get(username='johndoe1')
        self.url = reverse('profile')

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe1")

    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)