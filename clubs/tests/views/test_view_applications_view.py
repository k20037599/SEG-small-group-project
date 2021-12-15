""" tests of the applicant user list view """
from django.test import TestCase
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next
from django.conf import settings

class ViewApplicationsViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']

    """
    Gets the view_applications url
    and retrieves a valid officer and member
    """
    def setUp(self):
        self.url = reverse('view_applications')
        self.officer = User.objects.get(username='bobsmith1')
        self.member = User.objects.get(username='janedoe1')

    """
    Tests that view_applications url is correct
    """
    def test_view_applications_url(self):
        self.assertEqual(self.url, '/view_applications/')

    """
    creates a list of applications and tests to ensure
    that each application contains relevant information
    """
    def test_view_applications(self):
        self.client.login(username=self.officer.username, password='Password123')
        self._create_test_applicants(settings.USERS_PER_PAGE-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        for user_id in range(settings.USERS_PER_PAGE-1):
            self.assertContains(response, f'user{user_id}')
            user = User.objects.get(username=f'user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    """
    Ensures that unauthorised users (members) cannot see applicant list
    """
    def test_view_applications_by_unauthorised_user(self):
        self.client.login(username=self.member.username, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')

    """Test that the list of applicants is correcttly displayed in pages"""
    def test_get_applications_view_pagination(self):
        self.client.login(username=self.officer.username, password='Password123')
        self._create_test_applicants(settings.USERS_PER_PAGE*2+3-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)

        page_obj = response.context['users']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_one_url = reverse('view_applications') + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        page_obj = response.context['users']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_two_url = reverse('view_applications') + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), settings.USERS_PER_PAGE)
        page_obj = response.context['users']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())

        page_three_url = reverse('view_applications') + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 3)
        page_obj = response.context['users']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())

    """Test that the user is redirected when trying to view applicants when not logged in"""
    def test_get_view_applications_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    """
    creates test applicants
    """
    def _create_test_applicants(self, user_count=10):
        for user_id in range(user_count):
            User.objects.create_user(
                username = f'user{user_id}',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                email=f'user{user_id}@test.org',
                experience_level='BEGINNER',
                personal_statement='I am a beginner level player',
                bio=f'Bio {user_id}',
                password='Password123',
            )
