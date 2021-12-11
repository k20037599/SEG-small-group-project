from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class SignUpViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json']
    def setUp(self):
        self.url = reverse('home')

        self.test_user = User.objects.get(username='johndoe1')

    """
    Test whether the url is of the home url
    """
    def test_home_url(self):
        self.assertEqual(self.url, '/')

    """
    Tests whether calling a get on Home would return a 200 OK
    response and that the template used is "home.html"
    """
    def test_get_home(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "home.html")

    """
    Tests that that the user is redirected to their profile when they are already
    logged in and try to go to the home page
    """
    def test_get_home_redirects_when_logged_in(self):
        self.client.login(username=self.test_user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('profile')

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "profile.html")
