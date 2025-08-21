from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskForm(forms.ModelForm):
    """ Form for adding task on overview page. Check if input is valid. """
    class Meta:
        model = Task
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"required": False}),
            "description":
                forms.Textarea(attrs={"required": False, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # pass user in views
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        max_len = 50

        if len(title) == 0:
            raise ValidationError("This field cannot be empty.")
        if len(title) > 50:
            raise ValidationError(
                f"Title must be at most {max_len} characters."
            )
        user = self.user or getattr(self.instance, "user", None)
        if (
            user
            and Task.objects.filter(user=user, title__iexact=title)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError(
                "You already have a task with this name."
            )  # doesn't allow same title for the same user
        return title

    def clean_description(self):
        description = (self.cleaned_data.get("description") or "").strip()
        max_len = 300

        if len(description) == 0:
            raise ValidationError("This field cannot be empty.")
        if len(description) > 300:
            raise ValidationError(
                f"description must be at most {max_len} characters."
            )

        return description


class CustomSignupForm(SignupForm):
    """ Custom Sign up form to validate username length and uniqueness. """
    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()

        # Length check
        if len(username) < 8:
            raise ValidationError("Username must be at least 8 characters.")

        # uniqueness check
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                "That username is taken."
                "Please choose another one.")

        return super().clean_username()
