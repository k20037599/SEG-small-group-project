from django.test import TestCase, TransactionTestCase
from clubs.models import User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next

class ProfileViewTestCase(TransactionTestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']

    """
    Auxillary set up method which gets user: johndoe1
    and sets the profile url
    """
    def setUp(self):
        self.user = User.objects.get(username='johndoe1')
        self.url = reverse('profile')

    """
    Ensures that the profile url is correct
    """
    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    """
    Tests that when a user logs in with valid data,
    the profile is returned correctly.
    Checks that the response contains relevant data
    """
    def test_get_profile_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe1")

    """
    Tests that the user is redirected to the login page then back to the profile page
    when they try to access their profile when not logged in
    """
    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
