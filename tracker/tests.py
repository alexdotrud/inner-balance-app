from django.test import TestCase
from django.contrib.auth.models import User
from tracker.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_task_creation_and_str(self):
        task = Task.objects.create(user=self.user, title="My First Task")
        self.assertEqual(str(task), "My First Task (✗)")