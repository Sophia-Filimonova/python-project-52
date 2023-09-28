from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
# import pytest


class LoginMixinTestCase(TestCase):

    fixtures = ["users", "labels", "tasks", "statuses"]

    def setUp(self):
        self.urls = [
            reverse('user_update', kwargs={'pk': 1}),
            reverse('user_delete', kwargs={'pk': 1}),
            reverse('labels'),
            reverse('label_create'),
            reverse('label_update', kwargs={'pk': 1}),
            reverse('label_delete', kwargs={'pk': 1}),
            reverse('statuses'),
            reverse('status_create'),
            reverse('status_update', kwargs={'pk': 1}),
            reverse('status_delete', kwargs={'pk': 1}),
            reverse('tasks'),
            reverse('task_show', kwargs={'pk': 1}),
            reverse('task_create'),
            reverse('task_update', kwargs={'pk': 1}),
            reverse('task_delete', kwargs={'pk': 1}),
        ]

    def test_access_without_login(self):

        for url in self.urls:

            response = self.client.get(url, follow=False)
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('login'))

            response = self.client.get(url, follow=True)
            self.assertContains(
                response, _('You are not logged in! Please log in.'), status_code=200
            )
