""" tests of the member user list view """
from django.test import TestCase
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next
from django.conf import settings

class ViewMembersViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']

    """
    Gets the view_members url
    and retrieves a valid officer, applicant and member
    """
    def setUp(self):
        self.url = reverse('view_members')
        self.officer = User.objects.get(username='bobsmith1')
        self.member = User.objects.get(username='janedoe1')
        self.applicant = User.objects.get(username='johndoe1')

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
    def test_view_members_by_officer(self):
        self.client.login(username=self.officer.username, password='Password123')
        self._create_test_members(settings.USERS_PER_PAGE-2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-2):
            self.assertContains(response, f'user{user_id}')
            user = User.objects.get(username=f'user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    """
    Ensures that a list of members is generated with
    correct information and that members can view other
    members easily
    """
    def test_view_members_by_member(self):
        self.client.login(username=self.member.username, password='Password123')
        self._create_test_members(settings.USERS_PER_PAGE-2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-2):
            self.assertContains(response, f'user{user_id}')
            user = User.objects.get(username=f'user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    """
    Ensures that unauthorised users (applicants) cannot see member list
    """
    def test_view_members_by_unauthorised_user(self):
        self.client.login(username=self.applicant.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')

    """Test that the list of members is correcttly displayed in pages"""
    def test_view_members_pagination(self):
        self.client.login(username=self.officer.username, password='Password123')
        self._create_test_members(settings.USERS_PER_PAGE*2+3-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)

        page_obj = response.context['users']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_one_url = reverse('view_members') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        page_obj = response.context['users']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('view_members') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        page_obj = response.context['users']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('view_members') + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 4)
        page_obj = response.context['users']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    """Test that the user is redirected when trying to view members when not logged in"""
    def test_get_view_members_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    """
    Creates members for testing
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
