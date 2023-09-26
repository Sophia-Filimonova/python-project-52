from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import Label
from task_manager.helper import load_data
from task_manager.users.models import MyUser as User


class LabelsCrudTestCase(TestCase):

    fixtures = ["users", "labels", "tasks", "statuses"]

    def setUp(self):
        self.users = User.objects.all()
        self.client.force_login(self.users[1])
        self.labels = Label.objects.all()
        self.test_labels = load_data('test_data.json')["labels"]

    def test_create_label(self):
        response = self.client.get(reverse_lazy('label_create'))
        self.assertContains(response, _("Create label"), status_code=200)

        response = self.client.post(
            reverse_lazy('label_create'),
            self.test_labels["label1"],
            follow=True
        )
        self.assertContains(response, _('Label is successfully created'), status_code=200)
        self.assertTrue(Label.objects.filter(name=self.test_labels["label1"]["name"]).exists())

    def test_update_label(self):

        request_url = reverse_lazy('label_update', kwargs={'pk': self.labels[0].pk})

        new_name = self.labels[0].name + "-edited"
        response = self.client.post(
            request_url,
            {
                'name': new_name
            },
            follow=True
        )
        self.assertContains(response, _('Label is successfully changed'), status_code=200)
        self.assertTrue(Label.objects.filter(name=new_name).exists())

    def test_delete_label(self):

        request_url = reverse_lazy('label_delete', kwargs={'pk': self.labels[0].pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('Yes, delete'), status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            _('Unable to delete a label because it is in use'),
            status_code=200
        )

        request_url = reverse_lazy('label_delete', kwargs={'pk': self.labels[2].pk})
        name_deleted = self.labels[2].name
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, _('Label is successfully deleted'), status_code=200)

        self.assertFalse(Label.objects.filter(name=name_deleted).exists())

    def test_get_all_labels(self):

        response = self.client.get(reverse_lazy('labels'))
        for label in self.labels:
            self.assertContains(response, label.name)
