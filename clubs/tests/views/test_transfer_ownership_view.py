"""Tests for transfering ownership from owner to officer"""

from django.test import TestCase, Client
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next


class TransferOwnershipTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    """Creates test owner and officer to test feature."""

    def setUp(self):
        self.officer = User.objects.get(username='bobsmith1')
        self.owner = User.objects.get(username='jillbrown1')
        self.transfer_url = reverse('transfer_ownership', kwargs={
            'user_id': self.officer.id})

    """Tests that correct url is being used."""

    def test_transfer_ownership_url(self):
        self.assertEqual(self.transfer_url,
                         f'/transfer_ownership/{self.officer.id}')

    """Tests that after ownership is transferred, user is redirected to their updated profile"""

    def test_transfer_ownership_get(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.transfer_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    """Tests that no other user except owner can tranfer ownership"""

    def test_only_an_owner_can_transfer_ownership(self):
        self.member = User.objects.get(username='billysmith1')
        self.url = reverse('transfer_ownership', kwargs={
                           'user_id': self.officer.id})
        self.client.login(username=self.member.username,
                          password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    """Tests that owner can tranfer ownership correctly."""

    def test_owner_transfer_ownership(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.transfer_url)
        self.assertEqual(self.officer.user_type, "OFFICER")
        self.owner.transfer_ownership(self.officer)
        self.assertEqual(self.officer.user_type, "OWNER")

    """Tests that transferring ownership to an officer that doesn't exist redirects back to the user's profile"""

    def test_get_profile_with_invalid_id(self):
        self.client.login(username=self.owner.username, password='Password123')
        url = reverse('transfer_ownership', kwargs={
                      'user_id': self.officer.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
