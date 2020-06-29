from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from accountManagement.models import User

class StatisticsManagementTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(first_name="DisuraAdmin", username="dadm",
        email="disuraadminw@gmail.com", password="dadm123")
        User.objects.create_user(first_name="DisuraNormal", username="dnor",
        email="disuranormal@gmail.com", password="dnor123")

    def setUp(self):
        self.client = Client()

    def test_redirect_non_logged_in_user(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login/')
        
    def test_not_activated_user(self):
        User.objects.create_user(first_name="DisuraNotAct", username="dna",
        email="dna@gmail.com", password="dna123", activation_key="123456")
        self.client.login(username="dna", password="dna123")
        response = self.client.get(reverse('DailyRecords'), follow = True)
        self.assertTemplateUsed(response, 'activation/notActivated.html')
        response = self.client.get(reverse('TimelyRecords'), follow = True)
        self.assertTemplateUsed(response, 'activation/notActivated.html')