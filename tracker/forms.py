from django import forms
from .models import Task
from django.core.exceptions import ValidationError


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
