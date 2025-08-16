from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.timezone import now


class DailyReset(models.Model):
    last_reset = models.DateField(default=now)


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.TextField(blank=True)
    slug = models.SlugField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}"
            )  # automatically generates a slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'✓' if self.is_completed else '✗'})"
