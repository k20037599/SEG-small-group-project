from django.test import TestCase, TransactionTestCase
from clubs.models import User
from django.urls import reverse
from clubs.tests.helpers import reverse_with_next

class ShowUserViewTestCase(TransactionTestCase):
    fixtures = ['clubs/tests/fixtures/default_user.json', 'clubs/tests/fixtures/other_users.json']

    """
    Auxillary set up method which gets an Officer, Applicant and a member
    retrieves the urls for these users
    """
    def setUp(self):
        self.applicant = User.objects.get(username='johndoe1')
        self.member = User.objects.get(username='janedoe1')
        self.officer = User.objects.get(username='bobsmith1')
        self.applicant_url = reverse('show_user', kwargs={'user_id': self.applicant.id})
        self.member_url = reverse('show_user', kwargs={'user_id': self.member.id})
        self.officer_url = reverse('show_user', kwargs={'user_id': self.officer.id})

    """
    Tests whether these urls display correctly
    """
    def test_show_user_url(self):
        self.assertEqual(self.applicant_url,f'/show_user/{self.applicant.id}')
        self.assertEqual(self.member_url,f'/show_user/{self.member.id}')
        self.assertEqual(self.officer_url,f'/show_user/{self.officer.id}')

    """
    Tests whether a user can be rerieved using their id
    """
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

    """
    Ensures that officer can retrieve an applicant
    and view all their data
    """
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

    """
    Ensures that officer can retrieve an member
    and view all their data
    """
    def test_officer_get_member_profile(self):
        self.client.login(username=self.officer.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.member.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "janedoe1")
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "BEGINNER")
        self.assertContains(response, "I am a beginner level chess player")
        all_info = response.context['all_info']
        self.assertTrue(all_info)

    """
    Tests that trying to view a user profile with an
    invalid id is not allowed and the user is redirected
    """
    def test_get_profile_with_invalid_id(self):
        self.client.login(username=self.applicant.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.applicant.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')
