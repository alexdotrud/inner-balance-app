from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
User = get_user_model()

"""
Form for adding task on overview page.
"""
class TaskForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False
    )

    class Meta:
        model = Task
        fields = ["title", "description"]
        widgets = {
                "title": forms.TextInput(),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

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
