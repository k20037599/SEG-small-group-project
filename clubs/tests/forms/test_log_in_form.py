from django import forms
from django.test import TestCase
from clubs.forms import LogInForm


class LogInFormTestCase(TestCase):
    """
    An Auxillary set up method that contains valid form input data
    correspnding to the log in info for a user
    """
    def setUp(self):
        self.form_input = {'username': '@janedoe', 'password': 'Password123'}

    """
    Tests whether the form has required fields
    and also makes sure that password field widget is a PasswordInput widget
    """
    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    """
    Passes in correct input and asserts that it is valid
    """
    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    """
    User name should not be blank
    """
    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    """
    Password should not be blank
    """
    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    """
    The form should accept incorrect username input
    """
    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    """
    The form should accept incorrect password input
    """
    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
