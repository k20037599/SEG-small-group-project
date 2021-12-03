""" Some of these Tests Give Errors We need to look into it"""

"""Unit tests of the user form."""
from django import forms
from django.test import TestCase
from clubs.forms import UserForm
from clubs.models import User
from django.urls import reverse
from django.contrib import messages

class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.form_input = {
            'username': 'janedoe2',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.org',
            'personal_statement' : 'This is my personal Statement',
            'experience_level' : 'BEGINNER',
            'bio': 'Hello I am Jane',
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('personal_statement', form.fields)
        self.assertIn('experience_level', form.fields)
        self.assertIn('bio', form.fields)

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'a'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='janedoe1')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, 'janedoe2')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, 'Hello I am Jane')
