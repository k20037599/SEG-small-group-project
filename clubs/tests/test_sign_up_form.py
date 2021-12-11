from django.test import TestCase
from clubs.forms import SignUpForm
from django.core.exceptions import ValidationError
from clubs.models import User
from django import forms
from django.contrib.auth.hashers import check_password

class SignUpFormTestCase(TestCase):
    """
    An Auxillary set up method that contains valid form input data
    correspnding to a user
    """
    def setUp(self):
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username':'janedoe1',
            'password':'Password123',
            'password_confirm':'Password123',
            'experience_level':'BEGINNER',
            'email':'janedoe@example.com',
            'personal_statement':'I am a beginner level chess player',
            'bio':'hi i am jane'
        }

    """
    Passes in input data and then asserts that it is valid
    """
    def test_valid_sign_up_form(self):
        form=SignUpForm(data=self.form_input)

        self.assertTrue(form.is_valid())

    """
    Checks all the necessary fields of the form
    and checks that the password field uses a password widget
    """
    def test_form_has_right_fields(self):
        form = SignUpForm()

        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        pass_field = form.fields['password'].widget
        self.assertIn('password_confirm', form.fields)
        pass_confirm_field = form.fields['password_confirm'].widget
        self.assertTrue(isinstance(pass_field, forms.PasswordInput))
        self.assertTrue(isinstance(pass_confirm_field, forms.PasswordInput))
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('personal_statement', form.fields)
        self.assertIn('experience_level', form.fields)


    def test_password_contains_uppercase(self):
        self.form_input['password'] = "password123"
        self.form_input['password_confirm'] = "password123"
        form=SignUpForm(data=self.form_input)

        self.assertFalse(form.is_valid())

    def test_password_contains_lowercase(self):
        self.form_input['password'] = "PASSWORD123"
        self.form_input['password_confirm'] = "PASSWORD123"
        form=SignUpForm(data=self.form_input)

        self.assertFalse(form.is_valid())

    def test_password_contains_num(self):
        self.form_input['password'] = "Password"
        self.form_input['password_confirm'] = "Password"
        form=SignUpForm(data=self.form_input)

        self.assertFalse(form.is_valid())

    """
    Passes in unmatching password_confirm data to password_confirm field
    and then asserts it to be invalid
    """
    def test_password_and_password_confirm_are_identical(self):
        self.form_input['password_confirm'] = "Wrongpassword123"
        form=SignUpForm(data=self.form_input)

        self.assertFalse(form.is_valid())

    """
    Tests whether the user data is being saved correctly, by ensuring
    that the user count increases by 1
    and all the updated data matches the entered data
    """
    def test_form_saves_correctly(self):
        before_count = User.objects.count()
        form=SignUpForm(data=self.form_input)
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count,before_count+1)

        user = User.objects.get(username='janedoe1')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.com')
        self.assertEqual(user.bio, 'hi i am jane')
        self.assertEqual(user.experience_level, 'BEGINNER')
        self.assertEqual(user.personal_statement, 'I am a beginner level chess player')

        is_pass_correct = check_password('Password123', user.password)
        self.assertTrue(is_pass_correct)
