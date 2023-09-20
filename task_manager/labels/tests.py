from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import Label
from task_manager.helper import load_data
from task_manager.settings import test_english, remove_rollbar
from task_manager.users.models import MyUser as User


@test_english
@remove_rollbar
class LabelsCrudTestCase(TestCase):

    fixtures = ["users", "labels", "tasks", "statuses"]

    def setUp(self):
        self.users = User.objects.all()
        for user in self.users:
            user.set_password(user.password)
            user.save()

        self.client.force_login(self.users[1])
        self.labels = Label.objects.all()

    def test_create_label(self):
        response = self.client.get(reverse_lazy('label_create'))
        self.assertContains(response, _("Create label"), status_code=200)

        test_label = load_data('test_label.json')
        response = self.client.post(
            reverse_lazy('label_create'),
            test_label,
            follow=True
        )
        self.assertContains(response, _('Label is successfully created'), status_code=200)
        self.assertTrue(Label.objects.filter(name=test_label["name"]).exists())

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
        self.assertContains(response, self.labels[0].name, status_code=200)
        self.assertContains(response, self.labels[1].name)
        self.assertContains(response, self.labels[2].name)
