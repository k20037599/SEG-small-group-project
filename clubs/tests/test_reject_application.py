from django.test import TestCase, Client
from clubs.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from clubs.tests.helpers import reverse_with_next

class AcceptApplicationTestCase(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']
    def setUp(self):
        self.officer = User.objects.get(username='bobsmith1')
        self.applicant = User.objects.get(username='johndoe1')
        self.reject_url = reverse('reject_application', kwargs={'user_id': self.applicant.id})

    def test_reject_application_url(self):
        self.assertEqual(self.reject_url,f'/reject_application/{self.applicant.id}')

    def test_reject_application_get(self):
        self.client.login(username=self.officer.username, password='Password123')
        response = self.client.get(self.reject_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_only_an_officer_can_reject_applications(self):
        self.member = User.objects.get(username='billysmith1')
        self.url = reverse('reject_application', kwargs={'user_id': self.applicant.id})
        self.client.login(username=self.member.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_successful_reject_application(self):
        self.client.login(username=self.officer.username, password='Password123')
        response = self.client.get(self.reject_url)
        self.assertEqual(self.applicant.application_status, "PENDING")
        self.assertEqual(self.applicant.user_type, "APPLICANT")
        self.officer.reject_application(self.applicant)
        self.assertEqual(self.applicant.application_status, "REJECTED")
        self.assertEqual(self.applicant.user_type, "APPLICANT")

    def test_get_profile_with_invalid_id(self):
        self.client.login(username=self.officer.username, password='Password123')
        url = reverse('reject_application', kwargs={'user_id': self.applicant.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
