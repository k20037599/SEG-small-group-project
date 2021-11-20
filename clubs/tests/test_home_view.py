from django.test import TestCase
from django.urls import reverse
from clubs.models import User

class SignUpViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json']
    def setUp(self):
        self.url = reverse('home')

        self.test_user = User.objects.get(username='johndoe1')

    def test_home_url(self):
        self.assertEqual(self.url, '/')

    def test_get_home(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "home.html")

 ##login not implemented yet##
    # def test_get_home_redirects_when_logged_in(self):
    #     self.client.login(username=self.test_user.username, password="Password123")
    #     response = self.client.get(self.url, follow=True)
    #     redirect_url = reverse('feed')
    #
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, "feed.html")
