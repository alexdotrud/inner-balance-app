from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_reset = models.DateField(default=now)
    water_intake = models.FloatField(default=0)
    sleep_hours = models.FloatField(default=0)
    water_goal = models.FloatField(default=8.0)
    sleep_goal = models.FloatField(default=8.0)
    description = models.TextField(blank=True, default="")

    class Meta:

        pass
    