""" tests of the officers user list view """
from django.test import TestCase
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next


class ViewMembersViewTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('view_officers')
        self.officer = User.objects.get(username='bobsmith1')

    def test_view_officers_url(self):
        self.assertEqual(self.url, '/view_officers/')

    def test_get_view_officers_by_owner(self):
        self.client.login(username=self.owner.username, password='Password123')
        self._create_test_officers(15-2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15-2):
            self.assertContains(response, f'user{user_id}')
            user = User.objects.get(username=f'user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def test_get_view_officers_redirects_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, redirect_url,
                             status_code=302, target_status_code=200)

    def _create_test_officers(self, user_count=10):
        for user_id in range(user_count):
            User.objects.create_user(
                username=f'user{user_id}',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                email=f'user{user_id}@test.org',
                experience_level='BEGINNER',
                personal_statement='I am a beginner level player',
                bio=f'Bio {user_id}',
                user_type='OFFICER',
                password='Password123',
            )
