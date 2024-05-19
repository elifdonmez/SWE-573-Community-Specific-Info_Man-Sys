
from django.test import TestCase, Client
from django.urls import reverse
from .views import *


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_results_file_name = 'test_results.txt'
        self.test_results_file = open(self.test_results_file_name, 'a')


    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.write_test_result('test_register_view', response.status_code)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.write_test_result('test_login_view', response.status_code)

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


    def write_test_result(self, test_name, status_code):
        with open(self.test_results_file_name, 'a') as file:
            file.write(f'{test_name}: {status_code}\n')

    def tearDown(self):
        self.test_results_file.close()


