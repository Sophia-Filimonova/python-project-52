from django.test import TestCase
from .models import Task
import json
import os
from django.conf import settings
from task_manager.helpers import test_english, remove_rollbar
from task_manager.users.models import MyUser as User


@test_english
@remove_rollbar
class TasksCrudTestCase(TestCase):

    fixtures = ["users", "statuses", "labels", "tasks"]

    def setUp(self):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'users',
                'fixtures',
                'users.json'
            )
        ) as users_json:
            users_fixtures_data = users_json.read()

        self.users_data = json.loads(users_fixtures_data)

        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'tasks',
                'fixtures',
                'tasks.json'
            )
        ) as tasks_json:
            tasks_fixtures_data = tasks_json.read()

        self.tasks_data = json.loads(tasks_fixtures_data)

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )

    def test_create_task(self):

        response = self.client.get('/tasks/create/')
        self.assertContains(response, 'Create task', status_code=200)

        response = self.client.post(
            '/tasks/create/',
            {
                'name': "Testtask_3",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2,
            },
            follow=True
        )
        self.assertContains(response, 'Task is successfully created', status_code=200)
        self.assertTrue(Task.objects.filter(name="Testtask_3").exists())

    def test_update_task(self):

        request_url = '/tasks/' + str(self.tasks_data[0]['pk']) + '/update/'

        response = self.client.post(
            request_url,
            {
                'name': "Testtask_1-edited",
                'description': 'Test descriptrion',
                'status': 1,
                'executor': 2,
                'labels': [1, 2]
            },
            follow=True
        )
        self.assertContains(response, 'Task is successfully changed', status_code=200)
        self.assertTrue(Task.objects.filter(name="Testtask_1-edited").exists())

    def test_delete_task(self):

        request_url = '/tasks/' + str(self.tasks_data[0]['pk']) + '/delete/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'The task can be deleted only by its author', status_code=200)

        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'The task can be deleted only by its author', status_code=200)

        request_url = '/tasks/' + str(self.tasks_data[1]['pk']) + '/delete/'

        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Task is successfully deleted', status_code=200)

        self.assertFalse(Task.objects.filter(name=self.tasks_data[1]['fields']['name']).exists())

    def test_get_all_tasks(self):

        response = self.client.get('/tasks/')
        self.assertContains(response, self.tasks_data[0]['fields']['name'], status_code=200)
        self.assertContains(response, self.tasks_data[1]['fields']['name'])

        self.client.login(
            username=self.users_data[1]['fields']['username'],
            password=self.users_data[1]['fields']['password']
        )

        response = self.client.get(
            '/tasks/',
            {'status': '1', 'executor': '1', 'labels': '1', 'my_tasks': 'on'}
        )

        self.assertContains(response, self.tasks_data[0]['fields']['name'])
        self.assertNotContains(response, self.tasks_data[1]['fields']['name'])

        response = self.client.get(
            '/tasks/',
            {'status': 1, 'executor': 2, 'labels': 1, 'my_tasks': 'on'}
        )

        self.assertNotContains(response, self.tasks_data[0]['fields']['name'])
        self.assertNotContains(response, self.tasks_data[1]['fields']['name'])
