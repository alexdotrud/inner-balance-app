from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)