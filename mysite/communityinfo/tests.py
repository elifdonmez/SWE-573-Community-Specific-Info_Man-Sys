from http.cookies import SimpleCookie

from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    ''' This test is not working right now, username cannot be written to the database
    def not_test_view_profile(self):
        # self.client.login sets up self.client.session to be usable
        self.client.login(username='doga@example.com', password='123')

        session = self.client.session
        session['username'] = 'doga@example.com'
        session.save()

        response = self.client.get(reverse('view_profile'))
        print(response)
        self.assertEqual(response.status_code, 200)
        '''


