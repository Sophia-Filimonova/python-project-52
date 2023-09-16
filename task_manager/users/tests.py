from django.test import TestCase
from django.urls import reverse_lazy
import json
import os
from django.conf import settings
from task_manager.helpers import test_english, remove_rollbar
from .models import MyUser as User


@test_english
@remove_rollbar
class UserCrudTestCase(TestCase):

    fixtures = ["users"]

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        with open(os.path.join(
            settings.BASE_DIR,
            'task_manager',
            'users',
            'fixtures',
            'users.json'
        )) as users_json:
            users_fixtures_data = users_json.read()

        self.users_data = json.loads(users_fixtures_data)

    def test_create_user(self):

        response = self.client.get('/users/create/')
        self.assertContains(response, "Registration", status_code=200)

        response = self.client.post(
            '/users/create/',
            {
                'username': "Testuser1",
                'first_name': "Test",
                'last_name': "User",
                'password1': "33Test1122!",
                'password2': "33Test1122!",
            },
            follow=True
        )
        self.assertContains(response, 'User is created successfully', status_code=200)
        self.assertTrue(
            User.objects.filter(username="Testuser1").exists()
        )

        response = self.client.post(
            '/users/create/',
            {
                'username': "Testuser2",
                'first_name': "Test",
                'last_name': "User",
                'password1': "33Test1122!",
                'password2': "33Test1122!",
            },
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertTrue(
            User.objects.filter(username="Testuser2").exists()
        )

    def test_login(self):

        # response = self.client.post(
        #     '/login/',
        #     {
        #         'username': self.users_data[0]['fields']['username'],
        #         'password': "12321323"
        #     }
        # )
        # print(response.content)
        # self.assertContains(response, "Invalid username or password", status_code=200)

        response = self.client.get('/login/')
        self.assertContains(response, "Login", status_code=200)

        response = self.client.post(
            '/login/',
            {
                'username': self.users_data[0]['fields']['username'],
                'password': self.users_data[0]['fields']['password'],
            },
            follow=True
        )
        self.assertContains(response, "Exit", status_code=200)

        response = self.client.post(
            '/login/',
            {
                'username': self.users_data[0]['fields']['username'],
                'password': self.users_data[0]['fields']['password'],
            },
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('home'))

    def test_update_user(self):

        request_url = '/users/' + str(self.users_data[0]['pk']) + '/update/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You are not logged in! Please log in.', status_code=200)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You have no rights to change another user.', status_code=200)

        request_url = '/users/' + str(self.users_data[1]['pk']) + '/update/'

        response = self.client.post(
            request_url,
            {
                'username': self.users_data[1]['fields']['username'] + 'edit',
                'first_name': self.users_data[1]['fields']['first_name'] + 'edit',
                'last_name': self.users_data[1]['fields']['last_name'] + 'edit',
                'password1': self.users_data[1]['fields']['password'] + 'edit',
                'password2': self.users_data[1]['fields']['password'] + 'edit',
            },
            follow=True
        )
        self.assertContains(response, 'User is successfully updated', status_code=200)
        self.assertFalse(
            User.objects.filter(username=self.users_data[1]['fields']['username']).exists()
        )

    def test_delete_user(self):

        # user_id = User.objects.get(id=self.users_data[1]['pk']).id
        request_url = '/users/' + str(self.users_data[1]['pk']) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'You are not logged in! Please log in.', status_code=200)

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(response, 'You have no rights to delete another user.', status_code=200)

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(response, 'User is successfully deleted', status_code=200)

    def test_get_all_users(self):

        response = self.client.get('/users/')
        self.assertContains(response, self.users_data[0]['fields']['username'], status_code=200)
        self.assertContains(response, self.users_data[1]['fields']['username'])
