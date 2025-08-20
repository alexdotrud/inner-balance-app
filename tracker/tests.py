from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from tracker.models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        self.task = Task.objects.create(user=self.user, title="My Task")

    # Test the string representation of Task
    def test_str_method(self):
        self.assertEqual(str(self.task), "My Task (✗)")

    # Test that slug is automatically created
    def test_slug_created(self):
        self.assertTrue(self.task.slug.startswith("tester-my-task"))

class OverviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="password")

    # Test that anonymous users are redirected to login
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("tracker:overview"))
        self.assertEqual(response.status_code, 302)

    # Test that logged-in users can access the overview
    def test_logged_in_user_sees_page(self):
        self.client.login(username="tester", password="password")
        response = self.client.get(reverse("tracker:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tracker/overview.html")