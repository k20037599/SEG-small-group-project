""" tests of the member user list view """
from django.test import TestCase
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next

class ViewMembersViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']

    """
    Gets the view_members url
    and retrieves a valid officer
    """
    def setUp(self):
        self.url = reverse('view_members')
        self.officer = User.objects.get(username='bobsmith1')

    """
     Ensures that view_members url is correct
    """
    def test_view_members_url(self):
        self.assertEqual(self.url, '/view_members/')

    """
    Ensures that a list of members is generated with
    correct information and that officers can view
    members easily
    """
    def test_get_view_members_by_officer(self):
        self.client.login(username=self.officer.username, password='Password123')
        self._create_test_members(15-2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15-2):
            self.assertContains(response, f'user{user_id}')
            user = User.objects.get(username=f'user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)


    def test_get_view_members_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    """
    Creates 10 members for testing
    """
    def _create_test_members(self, user_count=10):
        for user_id in range(user_count):
            User.objects.create_user(
                username = f'user{user_id}',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                email=f'user{user_id}@test.org',
                experience_level='BEGINNER',
                personal_statement='I am a beginner level player',
                bio=f'Bio {user_id}',
                user_type='MEMBER',
                password='Password123',
            )
