"""Tests for transfering ownership from owner to officer"""

from django.test import TestCase, Client
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next


class TransferOwnershipTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    def setUp(self):
        self.officer = User.objects.get(username='bobsmith1')
        self.owner = User.objects.get(username='johndoe1')
        self.transfer_url = reverse('transfer_ownership', kwargs={
            'user_id': self.officer.id})

    def test_transfer_ownership_url(self):
        self.assertEqual(self.transfer_url,
                         f'/transfer_ownership/{self.officer.id}')

    # def test_promote_member_get(self):
    #     self.client.login(username=self.owner.username, password='Password123')
    #     response = self.client.get(self.promote_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'profile.html')

    def test_only_an_owner_can_transfer_ownership(self):
        self.member = User.objects.get(username='billysmith1')
        self.url = reverse('transfer_ownership', kwargs={
                           'user_id': self.officer.id})
        self.client.login(username=self.member.username,
                          password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # def test_owner_promote_member(self):
    #     self.client.login(username=self.owner.username, password='Password123')
    #     response = self.client.get(self.promote_url)
    #     self.assertEqual(self.member.user_type, "MEMBER")
    #     self.owner.promote_member(self.member)
    #     self.assertEqual(self.member.user_type, "OFFICER")

    def test_get_profile_with_invalid_id(self):
        self.client.login(username=self.owner.username, password='Password123')
        url = reverse('transfer_ownership', kwargs={
                      'user_id': self.officer.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
