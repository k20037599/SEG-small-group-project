"""Tests for promoting member to officer"""

from django.test import TestCase, Client
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next


class PromoteMemberTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json',
                'clubs/tests/fixtures/other_users.json']

    """Creates a test member and owner to test the feature."""

    def setUp(self):
        self.member = User.objects.get(username='janedoe1')
        self.owner = User.objects.get(username='jillbrown1')
        self.promote_url = reverse('promote_member', kwargs={
                                   'user_id': self.member.id})

    """Tests that the correct url is being used."""

    def test_promote_member_url(self):
        self.assertEqual(self.promote_url, f'/promote_member/{self.member.id}')

    """Tests that after promoting member, user is redirected to their updated profile."""

    def test_promote_member_get(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.promote_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    """Tests that owner is able to promote member to officer correctly."""

    def test_owner_promote_member(self):
        self.client.login(username=self.owner.username, password='Password123')
        response = self.client.get(self.promote_url)
        self.assertEqual(self.member.user_type, "MEMBER")
        self.owner.promote_member(self.member)
        self.assertEqual(self.member.user_type, "OFFICER")

    """Tests that promoting a member that doesn't exist redirects back to the user's profile"""

    def test_promote_member_with_invalid_id(self):
        self.client.login(username=self.owner.username, password='Password123')
        url = reverse('promote_member', kwargs={
                      'user_id': self.member.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url,
                             status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
