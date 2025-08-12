from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if len(title) > 50:
            raise forms.ValidationError("Title must be less than 50 characters.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if len(description) > 200:
            raise forms.ValidationError("Description must be less than 200 characters.")
        return description