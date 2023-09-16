from django.test import TestCase
from .models import Status
import json
import os
from django.conf import settings
from task_manager.helpers import test_english, remove_rollbar
from task_manager.users.models import MyUser as User


@test_english
@remove_rollbar
class StatusCrudTestCase(TestCase):

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

        self.client.login(
            username=self.users_data[0]['fields']['username'],
            password=self.users_data[0]['fields']['password']
        )

        with open(
            os.path.join(
                settings.BASE_DIR,
                'task_manager',
                'statuses',
                'fixtures',
                'statuses.json'
            )
        ) as tasks_json:
            statuses_fixtures_data = tasks_json.read()

        self.statuses_data = json.loads(statuses_fixtures_data)

    def test_create_status(self):

        response = self.client.get('/statuses/create/')
        self.assertContains(response, 'Create status', status_code=200)

        response = self.client.post(
            '/statuses/create/',
            {
                'name': "Teststatus_4"
            },
            follow=True
        )
        self.assertContains(response, 'Status is successfully created', status_code=200)
        self.assertTrue(Status.objects.filter(name="Teststatus_4").exists())

    def test_update_status(self):

        request_url = '/statuses/' + str(self.statuses_data[0]['pk']) + '/update/'

        response = self.client.post(
            request_url,
            {
                'name': "Teststatus_1-edited"
            },
            follow=True
        )
        self.assertContains(response, 'Status is successfully changed', status_code=200)
        self.assertTrue(Status.objects.filter(name="Teststatus_1-edited").exists())

    def test_delete_status(self):

        request_url = '/statuses/' + str(self.statuses_data[0]['pk']) + '/delete/'
        response = self.client.get(request_url, follow=True)
        self.assertContains(response, 'Yes, delete', status_code=200)
        response = self.client.post(request_url, follow=True)
        self.assertContains(
            response,
            'Unable to delete a status because it is in use',
            status_code=200
        )

        request_url = '/statuses/' + str(self.statuses_data[2]['pk']) + '/delete/'

        response = self.client.post(request_url, follow=True)
        self.assertContains(response, 'Status is successfully deleted', status_code=200)

        self.assertFalse(
            Status.objects.filter(name=self.statuses_data[2]['fields']['name']).exists()
        )

    def test_get_all_tasks(self):

        response = self.client.get('/statuses/')
        self.assertContains(response, self.statuses_data[0]['fields']['name'], status_code=200)
        self.assertContains(response, self.statuses_data[1]['fields']['name'])
        self.assertContains(response, self.statuses_data[2]['fields']['name'])
