"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from clubs.forms import UserForm
from clubs.models import User
from clubs.tests.helpers import reverse_with_next

class EditProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]
    """
    Auxillary set up method which gets user: janedoe1
    and fills a form_input with valid data
    """
    def setUp(self):
        self.url = reverse('edit_profile')
        self.user = User.objects.get(username='janedoe1')

        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'janedoe2',
            'password':'Password123',
            'password_confirm':'Password123',
            'email': 'janedoe@example.org',
            'bio': 'Hello I am Jane',
            'personal_statement' : 'This is my personal Statement',
            'experience_level' : 'BEGINNER',
        }

    """
    Asserts that it is the correct URL
    """
    def test_edit_profile_url(self):
        self.assertEqual(self.url, '/edit_profile/')

    """
    Tests whether the get request returns a 200 OK response
    and that the returned form is an instance of UserForm
    """
    def test_get_edit_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    """
    Passes in an invalid user name and tests that the
    view should not save the form
    The users profile data should be the same as before
    The total user count must remain the same as before
    """
    def test_unsuccessful_edit_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        form_input = self.form_input['username'] = 'a'
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('profile')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'janedoe1')
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'janedoe@example.org')
        self.assertEqual(self.user.bio, 'Hello I am Jane')

    """
    Tests a successful profile edit by passing in valid data
    And checking to see if it has been validated and saved correctly
    The total user count must remain the same as before
    """
    def test_successful_edit_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'janedoe2')
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'janedoe@example.org')
        self.assertEqual(self.user.bio, 'Hello I am Jane')

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
