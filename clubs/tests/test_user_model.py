from django.test import TestCase
from clubs.models import User
from django.core.exceptions import ValidationError

class UnitTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']
    def setUp(self):
        self.test_user = User.objects.get(username='johndoe1')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_valid_first_name(self):
        self.test_user.first_name = "Bob"

        self._assert_user_is_valid()

    def test_50char_first_name_is_valid(self):
        self.test_user.first_name = "x"*49

        self._assert_user_is_valid()

    def test_long_first_name_is_invalid(self):
        self.test_user.first_name = "x"*51

        self._assert_user_is_invalid()

    def test_first_name_doesnt_have_to_be_unique(self):
        second_user = User.objects.get(username='janedoe1')

        self.test_user.first_name = second_user.first_name

        self._assert_user_is_valid()

    def test_first_name_contains_non_alphanumeric_symbols(self):
        self.test_user.first_name = "Bob!£"

        self._assert_user_is_invalid()

    def test_first_name_contains_numbers(self):
        self.test_user.first_name = "Bob123"

        self._assert_user_is_invalid()

    def test_empty_first_name(self):
        self.test_user.first_name = ""

        self._assert_user_is_invalid()

    def test_valid_last_name(self):
        self.test_user.last_name = "Smith"

        self._assert_user_is_valid()

    def test_last_name_doesnt_have_to_be_unique(self):
        second_user = User.objects.get(username='janedoe1')

        self.test_user.last_name = second_user.last_name

        self._assert_user_is_valid()

    def test_50char_last_name_is_valid(self):
        self.test_user.last_name = "x"*49

        self._assert_user_is_valid()

    def test_long_last_name_is_invalid(self):
        self.test_user.last_name = "x"*51

        self._assert_user_is_invalid()

    def test_last_name_contains_non_alphanumeric_symbols(self):
        self.test_user.last_name = "Smith?#"

        self._assert_user_is_invalid()

    def test_last_name_contains_numbers(self):
        self.test_user.last_name = "Doe123"

        self._assert_user_is_invalid()

    def test_empty_last_name(self):
        self.test_user.last_name = ""

        self._assert_user_is_invalid()

    def test_valid_email(self):
        self.test_user.email = "bob@example.com"

        self._assert_user_is_valid()

    def test_email_with_no_username(self):
        self.test_user.email = "@example.com"

        self._assert_user_is_invalid()

    def test_email_with_no_at_symbol(self):
        self.test_user.email = "bob.com"

        self._assert_user_is_invalid()

    def test_email_with_no_domain_name(self):
        self.test_user.email = "bob@.com"

        self._assert_user_is_invalid()

    def test_email_with_no_dot(self):
        self.test_user.email = "bob@examplecom"

        self._assert_user_is_invalid()

    def test_email_is_unique(self):
        second_user = User.objects.get(username='janedoe1')

        self.test_user.email = second_user.email

        self._assert_user_is_invalid()

    def test_empty_email(self):
        self.test_user.email = ""

        self._assert_user_is_invalid()

    def test_email_with_no_domain_at_end(self):
        self.test_user.email = "bob@example"

        self._assert_user_is_invalid()

    def test_email_doesnt_contain_more_than_one_at_symbol(self):
        self.test_user.email = "bob@@example.com"

        self._assert_user_is_invalid()

    def test_valid_bio(self):
        self.test_user.bio = "Hello I'm Bob"

        self._assert_user_is_valid()

    def test_empty_bio(self):
        self.test_user.bio = ""

        self._assert_user_is_valid()

    def test_300char_bio_is_valid(self):
        self.test_user.bio = "x"*299

        self._assert_user_is_valid()

    def test_long_bio_is_invalid(self):
        self.test_user.bio = "x"*301

        self._assert_user_is_invalid()

    def test_valid_personal_statement(self):
        self.test_user.personal_statement = "Hello I'm Bob"

        self._assert_user_is_valid()

    def test_empty_personal_statement(self):
        self.test_user.personal_statement = ""

        self._assert_user_is_valid()

    def test_500char_personal_statement_is_valid(self):
        self.test_user.personal_statement = "x"*499

        self._assert_user_is_valid()

    def test_long_personal_statement_is_invalid(self):
        self.test_user.personal_statement = "x"*502

        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.test_user.full_clean()
        except (ValidationError):
            self.fail("Test user invalid")

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.test_user.full_clean()
