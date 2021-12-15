""" tests of the logout view """
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helpers import LogInTester
from django.contrib import messages

class LogoutViewTestCase(TestCase, LogInTester):
    fixtures = ['clubs/tests/fixtures/default_user.json']
    """
    Auxillary set up method which gets user: johndoe1
    and the log_out url
    """
    def setUp(self):
        self.url = reverse('log_out')
        self.test_user = User.objects.get(username='johndoe1')

    """
    Tests whether the logout url is correct
    """
    def test_logout_url(self):
        self.assertEqual(self.url, '/log_out/')

    """Tests that a logged in user can successfully log out"""
    def test_get_logout(self):
        self.client.login(username=self.test_user.username, password="Password123")
        self.assertTrue(self._is_logged_in())

        response = self.client.get(self.url, follow=True)

        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "home.html")

        self.assertFalse(self._is_logged_in())
