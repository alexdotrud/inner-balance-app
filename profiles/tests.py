from django.test import TestCase, Client
from .models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


class ProfileAvatarViewTest(TestCase):
    """Tests for the profile avatar upload view, ensuring that users can upload a valid avatar image."""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="tester", password="password")
        self.url = reverse("profiles:profile_avatar_view")  # adjust if your URL name is different
        self.client.login(username="tester", password="password")
        self.profile = UserProfile.objects.get(user=self.user)

    def test_valid_avatar_upload(self):
        # Create a simple fake image file
        image = SimpleUploadedFile(
            "avatar.png",
            b"fake image content",
            content_type="image/png"
        )
        response = self.client.post(self.url, {"avatar": image})
        self.profile.refresh_from_db()
        
        # Check that the avatar was updated
        self.assertTrue(self.profile.avatar.name.endswith("avatar.png"))
        self.assertRedirects(response, reverse("profiles:profile"))

class ProfileGoalUpdateTest(TestCase):
    """Test that updating goals in UserProfile saves correctly."""

    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password")
        self.profile = UserProfile.objects.create(user=self.user, water_goal=8, sleep_goal=8)

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
