from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from accountManagement.models import User

class SystemManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(first_name="DisuraAdmin", username="dadm",
        email="disuraadminw@gmail.com", password="dadm123")
        User.objects.create_user(first_name="DisuraNormal", username="dnor",
        email="disuranormal@gmail.com", password="dnor123")

    def setUp(self):
        self.client = Client()

    def test_redirect_non_logged_in_user(self):
        response = self.client.get(reverse('system_settings'), follow = True)
        self.assertRedirects(response, '/login/')
        response = self.client.get(reverse('user_settings'), follow = True)
        self.assertRedirects(response, '/login/')

    def test_redirect_nonadmin_user(self):
        self.client.login(username="dnor", password="dnor123")
        response = self.client.get(reverse('system_settings'))
        self.assertRedirects(response, '/?next=/system/system_settings')
        response = self.client.get(reverse('user_settings'))
        self.assertRedirects(response, '/?next=/system/user_settings')