from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_reset = models.DateField(default=now)
    water_intake = models.IntegerField(default=1)
    sleep_hours = models.FloatField(default=1)
    water_goal = models.IntegerField(default=8)
    sleep_goal = models.FloatField(default=8.0)
    description = models.TextField(blank=True, default="")

    class Meta:

        pass
    