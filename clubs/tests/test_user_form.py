""" Some of these Tests Give Errors We need to look into it"""

"""Unit tests of the user form."""
from django import forms
from django.test import TestCase
from clubs.forms import UserForm
from clubs.models import User
from django.urls import reverse
from django.contrib import messages
from clubs.tests.helpers import reverse_with_next

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/other_users.json'
    ]

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
            'bio': 'My bio',
            'personal_statement' : 'This is my personal Statement',
            'experience_level' : 'BEGINNER',
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)

    def test_successful_edit_profile(self):
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
        self.assertEqual(self.user.bio, 'My bio')

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
        self.assertEqual(self.user.bio, 'My bio')

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
