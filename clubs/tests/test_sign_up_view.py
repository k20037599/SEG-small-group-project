""" tests of the sign up view """
from django.test import TestCase
from clubs.forms import SignUpForm
from django.urls import reverse
from clubs.models import User
from django.contrib.auth.hashers import check_password
#from clubs.tests.helpers import LoginTester


class SignUpViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('sign_up')

        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe1',
            'password': 'Password123',
            'password_confirm': 'Password123',
            'experience_level': 'BEGINNER',
            'email': 'janedoe@example.com',
            'personal_statement': 'I am a beginner level chess player',
            'bio': 'hi i am jane'
        }

        self.test_user = User.objects.get(username='johndoe1')

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "sign_up.html")

        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    ##not implemented login yet##

    # def test_unsuccesful_sign_up(self):
    #     self.form_input['username'] = "bad_username"
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count,before_count)
    #     self.assertEqual(response.status_code, 200)
    #
    #     self.assertTemplateUsed(response, "sign_up.html")
    #
    #     form = response.context['form'];
    #     self.assertTrue(isinstance(form, SignUpForm))
    #     self.assertTrue(form.is_bound)
    #     self.assertFalse(self._is_logged_in())
    #
    #     self.assertFalse(self._is_logged_in())
    #
    # def test_succesful_sign_up(self):
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count,before_count+1)
    #     response_url = reverse('feed')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #
    #     self.assertTemplateUsed(response, "feed.html")
    #
    #     user = User.objects.get(username='janedoe1')
    #     self.assertEqual(user.first_name, 'Jane')
    #     self.assertEqual(user.last_name, 'Doe')
    #     self.assertEqual(user.email, 'janedoe@example.com')
    #     self.assertEqual(user.bio, 'hi i am jane')
    #
    #     is_pass_correct = check_password('Password123', user.password)
    #     self.assertTrue(is_pass_correct)
    #     self.assertTrue(self._is_logged_in())
    #
    #     self.assertTrue(self._is_logged_in())

    # def test_get_sign_up_redirects_when_logged_in(self):
    #     self.client.login(username=self.test_user.username, password="Password123")
    #     response = self.client.get(self.url, follow=True)
    #     redirect_url = reverse('feed')
    #
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, "feed.html")
    #
    # def test_post_get_sign_up_redirects_when_logged_in(self):
    #     before_count = User.objects.count()
    #     self.client.login(username=self.test_user.username, password="Password123")
    #     response = self.client.get(self.url, self.form_input, follow=True)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count,before_count)
    #     redirect_url = reverse('feed')
    #
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, "feed.html")
