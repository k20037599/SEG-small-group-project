from django.test import TestCase, TransactionTestCase
from clubs.models import User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next

class ProfileViewTestCase(TransactionTestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']
    def setUp(self):
        self.applicant = User.objects.get(username='johndoe1')
        self.member = User.objects.get(username='janedoe1')
        self.officer = User.objects.get(username='bobsmith1')
        self.applicant_url = reverse('show_user', kwargs={'user_id': self.applicant.id})

    def test_profile_url(self):
        self.assertEqual(self.applicant_url,f'/show_user/{self.applicant.id}')

    def test_get_profile_with_valid_id(self):
        self.client.login(username=self.officer.username, password='Password123')
        response = self.client.get(self.applicant_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe1")

    def test_get_profile_with_own_id(self):
        self.client.login(username=self.officer.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.officer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "Bob Smith")
        self.assertContains(response, "bobsmith1")
        all_info = response.context['all_info']
        self.assertFalse(all_info)

    def test_officer_get_applicant_profile(self):
        self.client.login(username=self.officer.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.applicant.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe1")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "BEGINNER")
        self.assertContains(response, "I am a beginner level chess player")
        all_info = response.context['all_info']
        self.assertTrue(all_info)

    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get(self.applicant_url)
        redirect_url = reverse_with_next('log_in', self.applicant_url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_applicant_profile_with_invalid_id(self):
        self.client.login(username=self.applicant.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.applicant.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
