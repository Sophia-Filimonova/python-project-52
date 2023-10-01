from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.helper import load_data
from .models import Status
from task_manager.users.models import MyUser as User


class StatusCrudTestCase(TestCase):

    fixtures = ["users", "statuses", "labels", "tasks"]

    def setUp(self):
        self.users = User.objects.all()
        self.client.force_login(self.users[0])
        self.statuses = Status.objects.all()
        self.test_statuses = load_data('test_data.json')["statuses"]

    def test_create_status(self):

        response = self.client.get(reverse_lazy('status_create'))
        self.assertContains(response, _('Create status'), status_code=200)

        response = self.client.post(
            reverse_lazy('status_create'),
            self.test_statuses["new"],
            follow=True
        )
        self.assertContains(response, _('Status is successfully created'), status_code=200)
        self.assertTrue(Status.objects.filter(name=self.test_statuses["new"]["name"]).exists())

    def test_update_status(self):

        status1 = self.statuses[0]
        request_url = reverse_lazy('status_update', kwargs={'pk': status1.pk})
        new_name = status1.name + "-edited"
        response = self.client.post(
            request_url,
            {
                'name': new_name
            },
            follow=True
        )
        self.assertContains(response, _('Status is successfully changed'), status_code=200)
        self.assertTrue(Status.objects.filter(name=new_name).exists())

    def test_delete_status_in_use(self):

        status1 = self.statuses[0]
        request_url = reverse_lazy('status_delete', kwargs={'pk': status1.pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('Yes, delete'), status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            _('Unable to delete a status because it is in use'),
            status_code=200
        )

    def test_delete_status_successfully(self):

        status3 = self.statuses[2]
        request_url = reverse_lazy('status_delete', kwargs={'pk': status3.pk})
        name_deleted = status3.name
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, _('Status is successfully deleted'), status_code=200)
        self.assertFalse(
            Status.objects.filter(name=name_deleted).exists()
        )

    def test_get_all_statuses(self):

        response = self.client.get(reverse_lazy('statuses'))
        for status in self.statuses:
            self.assertContains(response, status.name)
