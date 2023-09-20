from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.helper import load_data
from .models import Status
from task_manager.settings import test_english, remove_rollbar
from task_manager.users.models import MyUser as User


@test_english
@remove_rollbar
class StatusCrudTestCase(TestCase):

    fixtures = ["users", "statuses", "labels", "tasks"]

    def setUp(self):
        self.users = User.objects.all()
        for user in self.users:
            user.set_password(user.password)
            user.save()

        self.client.force_login(self.users[0])
        self.statuses = Status.objects.all()

    def test_create_status(self):

        response = self.client.get(reverse_lazy('status_create'))
        self.assertContains(response, _('Create status'), status_code=200)

        test_status = load_data('test_status.json')
        response = self.client.post(
            reverse_lazy('status_create'),
            test_status,
            follow=True
        )
        self.assertContains(response, _('Status is successfully created'), status_code=200)
        self.assertTrue(Status.objects.filter(name=test_status["name"]).exists())

    def test_update_status(self):

        request_url = reverse_lazy('status_update', kwargs={'pk': self.statuses[0].pk})

        new_name = self.statuses[0].name + "-edited"
        response = self.client.post(
            request_url,
            {
                'name': new_name
            },
            follow=True
        )
        self.assertContains(response, _('Status is successfully changed'), status_code=200)
        self.assertTrue(Status.objects.filter(name=new_name).exists())

    def test_delete_status(self):

        request_url = reverse_lazy('status_delete', kwargs={'pk': self.statuses[0].pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('Yes, delete'), status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            _('Unable to delete a status because it is in use'),
            status_code=200
        )

        request_url = reverse_lazy('status_delete', kwargs={'pk': self.statuses[2].pk})
        name_deleted = self.statuses[2].name
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, _('Status is successfully deleted'), status_code=200)

        self.assertFalse(
            Status.objects.filter(name=name_deleted).exists()
        )

    def test_get_all_tasks(self):

        response = self.client.get(reverse_lazy('statuses'))
        self.assertContains(response, self.statuses[0].name, status_code=200)
        self.assertContains(response, self.statuses[1].name)
        self.assertContains(response, self.statuses[2].name)
