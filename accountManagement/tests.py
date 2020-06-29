from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .models import User

class AccountManagementTests(TestCase):

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

    def test_login_user(self):
        self.client.login(username="dnor", password="dnor123")
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_not_activated_user(self):
        User.objects.create_user(first_name="DisuraNotAct", username="dna",
        email="dna@gmail.com", password="dna123", activation_key="123456")
        self.client.login(username="dna", password="dna123")
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'activation/notActivated.html')

    def test_redirect_nonadmin_on_register(self):
        self.client.login(username="dnor", password="dnor123")
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, '/?next=/register/')

    def test_registration_form_errors(self):
        self.client.login(username="dadm", password="dadm123")
        fname = "Dummy"
        # duplicate username
        response = self.client.post(reverse('register'), {'username':'dadm'})
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
        # duplicate email
        response = self.client.post(reverse('register'), {'email':'disuraadminw@gmail.com'})
        self.assertFormError(response, 'form', 'email', 'That email is already being used by another user.')
        # mismatching passwords
        response = self.client.post(reverse('register'), {'password1':'dddd', 'password2' : 'dddc'})
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")
        # required fields empty
        response = self.client.post(reverse('register'), {})
        self.assertFormError(response, 'form', 'username', "This field is required.")
        self.assertFormError(response, 'form', 'first_name', "This field is required.")
        self.assertFormError(response, 'form', 'email', "This field is required.")
        self.assertFormError(response, 'form', 'password1', "This field is required.")
        self.assertFormError(response, 'form', 'password2', "This field is required.")

    def test_restrict_delete_admin(self):
        # deleting the admin by admin himself
        self.client.login(username="dadm", password="dadm123")
        user_id = User.objects.get(is_staff=True).id
        response = self.client.get('userremove/{}'.format(user_id))
        self.assertEquals(response.status_code, 404)
        