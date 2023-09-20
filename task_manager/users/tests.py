from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.helper import load_data
from task_manager.settings import test_english, remove_rollbar
from .models import MyUser as User


@test_english
@remove_rollbar
class UserCrudTestCase(TestCase):

    fixtures = ["users"]

    def setUp(self):
        self.passwords_dict = {}
        self.users = User.objects.all()
        for user in self.users:
            self.passwords_dict[user.pk] = user.password
            user.set_password(user.password)
            user.save()

    def test_create_user(self):

        test_users = load_data('test_users.json')
        response = self.client.get(reverse_lazy('user_create'))
        self.assertContains(response, _('Registration'), status_code=200)

        response = self.client.post(
            reverse_lazy('user_create'),
            test_users[0],
            follow=True
        )
        self.assertContains(response, _('User is created successfully'), status_code=200)
        self.assertTrue(
            User.objects.filter(username=test_users[0]["username"]).exists()
        )

        response = self.client.post(
            reverse_lazy('user_create'),
            test_users[1],
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertTrue(
            User.objects.filter(username=test_users[1]["username"]).exists()
        )

    def test_login(self):

        response = self.client.get(reverse_lazy('login'))
        self.assertContains(response, _('Login'), status_code=200)

        response = self.client.post(
            reverse_lazy('login'),
            {
                "username": self.users[0].username,
                "password": self.passwords_dict[self.users[0].pk],
            },
            follow=True
        )
        self.assertContains(response, _('Exit'), status_code=200)

        response = self.client.post(
            reverse_lazy('login'),
            {
                'username': self.users[0].username,
                'password': self.passwords_dict[self.users[0].pk],
            },
            follow=False
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('home'))

    def test_update_user(self):

        request_url = reverse_lazy('user_update', kwargs={'pk': self.users[0].pk})

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('You are not logged in! Please log in.'), status_code=200)

        self.client.force_login(self.users[1])
        response = self.client.get(request_url, follow=True)
        self.assertContains(
            response,
            _('You have no rights to change another user.'),
            status_code=200
        )

        request_url = reverse_lazy('user_update', kwargs={'pk': self.users[1].pk})
        old_name = self.users[1].username
        response = self.client.post(
            request_url,
            {
                'username': self.users[1].username + '-edited',
                'first_name': self.users[1].first_name + '-edited',
                'last_name': self.users[1].last_name + '-edited',
                'password1': self.users[1].password + '-edited',
                'password2': self.users[1].password + '-edited',
            },
            follow=True
        )
        self.assertContains(response, _('User is successfully updated'), status_code=200)
        self.assertFalse(
            User.objects.filter(username=old_name).exists()
        )

    def test_delete_user(self):

        request_url = reverse_lazy('user_delete', kwargs={'pk': self.users[1].pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('You are not logged in! Please log in.'), status_code=200)

        self.client.force_login(self.users[0])
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(
            response,
            _('You have no rights to delete another user.'),
            status_code=200
        )

        self.client.force_login(self.users[1])
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(response, _('User is successfully deleted'), status_code=200)

    def test_get_all_users(self):

        response = self.client.get(reverse_lazy('users'))
        self.assertContains(response, self.users[0].username, status_code=200)
        self.assertContains(response, self.users[1].username)
