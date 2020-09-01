from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from accountManagement.models import User
from selenium import webdriver
from statisticsManagement.controllers import saveAllToDatabase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

class TestPrediction(StaticLiveServerTestCase):

    def setUp(self):
        User.objects.create_superuser(first_name="Thuvarakan", username="thuva",
        email="thuva1000@gmail.com", password="thuva97")
        saveAllToDatabase(timely_filename="2020-06-01 to 2020-06-14 timely.txt", daily_filename="2020-06-01 to 2020-06-14 daily.txt")
        self.browser = webdriver.Chrome("chromedriver.exe")

    def teardown(self):
        self.browser.close()
    
    def test_non_loggedinUser_trying_predictionUrl(self):
        prediction_url = self.live_server_url + reverse('Prediction')
        self.browser.get(prediction_url)
        #must return to login page
        
    def test_login_and_predictionLink(self):
        self.browser.get(self.live_server_url)
        prediction_url = self.live_server_url + reverse('Prediction')
        username = self.browser.find_element_by_name("username").send_keys('thuva')
        password = self.browser.find_element_by_name("password").send_keys('thuva97')
        submit = self.browser.find_element_by_class_name("btn").submit()

        self.browser.find_element_by_id("predictionButton").click()
        self.assertEquals(
            self.browser.current_url,
            prediction_url
        )
        #must loggedin and navigate to "/prediction/" url

class PredictionTests(TestCase):

    def setUp(self):
        User.objects.create_superuser(first_name="Thuvarakan", username="thuva",
        email="thuva1000@gmail.com", password="thuva97")
        self.client = Client()

    def test_loggedin_user(self):
        self.client.login(username="thuva", password="thuva97")
        response = self.client.get(reverse('Prediction'))
        self.assertTemplateUsed(response, 'Analysis.html')
    
    def test_getpre_post(self):
        self.client.login(username="thuva", password="thuva97")
        response = self.client.post(reverse('getPre'), {'startDate':'2020-06-14', 'endDate' : '2020-06-20'})        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'prediction.html')
        # restrictions for startdate and enddate is done in frontend using JS

    

