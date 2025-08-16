from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


def avatar_upload_path(instance, filename):
    return f"avatars/user_{instance.user_id}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
       upload_to=avatar_upload_path,
       blank=True,
       null=True,
    )
    last_reset = models.DateField(default=now)
    water_intake = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    sleep_hours = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(20)]
    )

    water_goal = models.FloatField(
        default=8.0, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    sleep_goal = models.FloatField(
        default=8.0, validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    description = models.TextField(blank=True, default="")

    class Meta:

        pass
