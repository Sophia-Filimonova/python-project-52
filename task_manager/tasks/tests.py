from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.helper import load_data
from .models import Task
from task_manager.users.models import MyUser as User


class TasksCrudTestCase(TestCase):

    fixtures = ["users", "statuses", "labels", "tasks"]

    def setUp(self):
        self.users = User.objects.all()
        self.client.force_login(self.users[0])
        self.tasks = Task.objects.all()
        self.test_tasks = load_data('test_data.json')["tasks"]

    def test_create_task(self):
        response = self.client.get(reverse_lazy('task_create'))
        self.assertContains(response, _('Create task'), status_code=200)

        response = self.client.post(
            reverse_lazy('task_create'),
            self.test_tasks["new"],
            follow=True
        )
        self.assertContains(response, _('Task is successfully created'), status_code=200)
        self.assertTrue(Task.objects.filter(name=self.test_tasks["new"]["name"]).exists())

    def test_update_task(self):

        task1 = self.tasks[0]
        request_url = reverse_lazy('task_update', kwargs={'pk': task1.pk})
        old_name = task1.name
        response = self.client.post(
            request_url,
            {
                'name': task1.name + '-edited',
                'description': task1.description + '-edited',
                'status': task1.status.pk,
                'executor': task1.executor.pk,
                'labels': [1, 2],
            },
            follow=True
        )
        self.assertContains(response, _('Task is successfully changed'), status_code=200)
        self.assertFalse(Task.objects.filter(name=old_name).exists())

    def test_delete_task_not_by_author(self):

        task1 = self.tasks[0]
        request_url = reverse_lazy('task_delete', kwargs={'pk': task1.pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(
            response,
            _('The task can be deleted only by its author'),
            status_code=200
        )
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            _('The task can be deleted only by its author'),
            status_code=200
        )

    def test_delete_task_successfully(self):

        task2 = self.tasks[1]
        request_url = reverse_lazy('task_delete', kwargs={'pk': task2.pk})
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, _('Yes, delete'), status_code=200)
        name_deleted = task2.name
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, _('Task is successfully deleted'), status_code=200)
        self.assertFalse(Task.objects.filter(name=name_deleted).exists())

    def test_get_all_tasks(self):

        response = self.client.get(reverse_lazy('tasks'))
        for task in self.tasks:
            self.assertContains(response, task.name)

    def test_get_filtered_tasks(self):

        self.client.force_login(self.users[1])

        response = self.client.get(
            reverse_lazy('tasks'),
            {'status': '1', 'executor': '1', 'labels': '1', 'my_tasks': 'on'}
        )

        self.assertContains(response, self.tasks[0].name)
        self.assertNotContains(response, self.tasks[1].name)

        response = self.client.get(
            reverse_lazy('tasks'),
            {'status': 1, 'executor': 2, 'labels': 1, 'my_tasks': 'on'}
        )

        self.assertNotContains(response, self.tasks[0].name)
        self.assertNotContains(response, self.tasks[1].name)
