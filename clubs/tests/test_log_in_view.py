"""Tests of the log in view."""
from django.test import TestCase
from django.urls import reverse
from clubs.forms import LogInForm
from clubs.models import User
from clubs.tests.helpers import LogInTester, reverse_with_next
from django.contrib import messages


class LogInViewTestCase(TestCase, LogInTester):
    fixtures = ['clubs/tests/fixtures/default_user.json']

    """
    Auxillary set up method which gets user: johndoe1
    and fills a form_input with valid data for log in
    """
    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username='johndoe1')
        self.form_input = {'username': 'johndoe1', 'password': 'Password123'}

    """
    Tests whether the login url is correct
    """
    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    """
    Tests whether the GET request on login is Ok (200)
    """
    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """
    Passes in an incorrect password and ensures that such a login request
    does not go through
    """
    def test_unsuccesful_log_in(self):
        form_input = {'username': '@johndoe', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    """
    Passes in correct login data and checks that the login goes through
    """
    def test_succesful_log_in(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('profile')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    """
    Tests whether the log_in page correctly redirects to the
    users profile page
    """
    def test_get_log_in_with_redirect(self):
        dest_url = reverse('profile')
        self.url = reverse_with_next('log_in', dest_url)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "log_in.html")

        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

        self.assertEqual(next, dest_url)

        messages_list = list(response.context['messages'])

        self.assertEqual(len(messages_list), 0)

    """
    Ensures that a redirect response is given when the user
    Successfully logs in (should redirect to profile)
    """
    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('profile')

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "profile.html")

    """
    Passes in valid information and assert that it redirects
    after log in
    """
    def test_successful_login_with_redirect(self):
        redirect_url = reverse('profile')
        form_input = {'username': 'johndoe1', 'password': 'Password123', 'next':redirect_url}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "profile.html")

        messages_list = list(response.context['messages'])

        self.assertEqual(len(messages_list), 0)


    def test_post_get_login_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        form_input = {'username':"wronguser", 'password':"wrongpass"}
        response = self.client.get(self.url, form_input, follow=True)
        redirect_url = reverse('profile')

        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "profile.html")


    def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('profile')
        form_input = { 'username': 'johndoe1', 'password': 'WrongPassword123', 'next': redirect_url }
        response = self.client.post(self.url, form_input)
        next = response.context['next']

        self.assertEqual(next, redirect_url)

    """
    Ensures that an inactive user can log in
    """
    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
