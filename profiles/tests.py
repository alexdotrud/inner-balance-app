from django.test import TestCase
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileAvatarTest(TestCase):
    """Test that the profile page renders and includes avatar functionality."""

    def setUp(self):
        self.user = User.objects.create_user("tester", password="pass123")
        self.client.login(username="tester", password="pass123")
        UserProfile.objects.create(user=self.user)

    def test_profile_page_renders_avatar(self):
        url = reverse("profiles:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # If no avatar, you expect fallback / None
        self.assertIn("username", response.context)
        self.assertIn("profile", response.context)


class ProfileGoalUpdateTest(TestCase):
    """Test that updating goals in UserProfile saves correctly."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="password"
    )
        self.profile = UserProfile.objects.create(
            user=self.user, water_goal=8, sleep_goal=8
        )

    def test_update_goals(self):
        # Update goals
        self.profile.water_goal = 10
        self.profile.sleep_goal = 7.5
        self.profile.save()

        # Refresh from database
        self.profile.refresh_from_db()

        # Check values
        self.assertEqual(self.profile.water_goal, 10)
        self.assertEqual(self.profile.sleep_goal, 7.5)
