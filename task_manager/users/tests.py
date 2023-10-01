from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.helper import load_data
from .models import MyUser as User


class UserCrudTestCase(TestCase):

    fixtures = ["users"]

    def setUp(self):
        self.users = User.objects.all()
        self.test_users = load_data('test_data.json')['users']

    def test_create_user(self):

        response = self.client.get(reverse_lazy('user_create'))
        self.assertContains(response, _('Registration'), status_code=200)

        response = self.client.post(
            reverse_lazy('user_create'),
            self.test_users["new"],
            follow=True
        )
        self.assertContains(response, _('User is created successfully'), status_code=200)
        self.assertTrue(
            User.objects.filter(username=self.test_users["new"]["username"]).exists()
        )

        response = self.client.post(
            reverse_lazy('user_create'),
            self.test_users["new"],
            follow=True
        )
        self.assertContains(
            response,
            _('A user with that username already exists.'),
            status_code=200
        )

    def test_update_another_user(self):

        user1 = self.users[0]
        user2 = self.users[1]
        request_url = reverse_lazy('user_update', kwargs={'pk': user1.pk})

        self.client.force_login(user2)
        response = self.client.get(request_url, follow=True)
        self.assertContains(
            response,
            _('You have no rights to change another user.'),
            status_code=200
        )

    def test_update_user_successfully(self):

        user2 = self.users[1]
        self.client.force_login(user2)
        request_url = reverse_lazy('user_update', kwargs={'pk': user2.pk})
        response = self.client.post(
            request_url,
            {
                'username': user2.username,
                'first_name': user2.first_name + '-edited',
                'last_name': user2.last_name + '-edited',
                'password1': user2.password,
                'password2': user2.password,
            },
            follow=True
        )
        self.assertContains(response, _('User is successfully updated'), status_code=200)
        self.assertTrue(
            User.objects.filter(first_name=user2.first_name + '-edited').exists()
        )

    def test_delete_another_user(self):

        user1 = self.users[0]
        user2 = self.users[1]
        request_url = reverse_lazy('user_delete', kwargs={'pk': user1.pk})
        self.client.force_login(user2)
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(
            response,
            _('You have no rights to delete another user.'),
            status_code=200
        )

    def test_delete_user_successfully(self):

        user1 = self.users[0]
        request_url = reverse_lazy('user_delete', kwargs={'pk': user1.pk})
        self.client.force_login(user1)
        response = self.client.post(request_url, {}, follow=True)
        self.assertContains(response, _('User is successfully deleted'), status_code=200)

    def test_get_all_users(self):

        response = self.client.get(reverse_lazy('users'))
        for user in self.users:
            self.assertContains(response, user.username)
