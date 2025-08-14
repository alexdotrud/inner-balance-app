from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
User = get_user_model()

"""
Form for adding task on overview page. Check if input is empty or too long.
"""
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 50,}),
            "description": forms.Textarea(attrs={"maxlength": 300, "rows": 3}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if len(title) == 0:
            raise ValidationError("This field cannot be empty.")
        if len(title) > 50:
            raise ValidationError("Title must be less than or equal to 50 characters.")
        return title

    def clean_description(self):
        description = (self.cleaned_data.get("description") or "").strip()
        if len(description) == 0:
            raise ValidationError("This field cannot be empty.")
        if len(description) > 300:
            raise ValidationError("Description must be less than or equal to 300 characters.")
        return description
    

class CustomSignupForm(SignupForm):
    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        
        # Length check
        if len(username) < 8:
            raise ValidationError("Username must be at least 8 characters long.")
        
        # uniqueness check
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("That username is taken. Please choose another one.")

        
        return super().clean_username()
