"""Tests for demoting officer to member"""

from django.test import TestCase, Client
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next


class DemoteOfficerTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    """Creates a test officer and owner to test the feature."""

    def setUp(self):
        self.officer = User.objects.get(username='bobsmith1')
        self.owner = User.objects.get(username='jillbrown1')
        self.demote_url = reverse('demote_officer', kwargs={
            'user_id': self.officer.id})

    """Tests that the correct url is being used."""

    def test_demote_officer_url(self):
        self.assertEqual(self.demote_url, f'/demote_officer/{self.officer.id}')

    """Tests that after demoting officer, user is redirected to their updated profile."""

    def test_demote_officer_get(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.demote_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    """Tests that no other user except an owner is able to demote an officer."""

    def test_only_an_owner_can_demote_officer(self):
        self.member = User.objects.get(username='billysmith1')
        self.url = reverse('demote_officer', kwargs={
                           'user_id': self.officer.id})
        self.client.login(username=self.member.username,
                          password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    """Tests that owner is able to demote officer correctly."""

    def test_owner_demote_officer(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.demote_url)
        self.assertEqual(self.officer.user_type, "OFFICER")
        self.owner.demote_officer(self.officer)
        self.assertEqual(self.officer.user_type, "MEMBER")

    """Tests that demoting an officer that doesn't exist redirects back to the user's profile"""

    def test_get_profile_with_invalid_id(self):
        self.client.login(username=self.owner.username, password='Password123')
        url = reverse('demote_officer', kwargs={
                      'user_id': self.officer.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
