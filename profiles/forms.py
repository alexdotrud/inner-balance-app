from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["description", "water_goal", "sleep_goal"]

    def clean_water_goal(self):
        val = self.cleaned_data.get("water_goal")
        if val is None or val < 0 or val > 20:
            raise forms.ValidationError("Water goal must be between 0 and 20.")
        return val

    def clean_sleep_goal(self):
        val = self.cleaned_data.get("sleep_goal")
        if val is None or val < 0 or val > 20:
            raise forms.ValidationError("Sleep goal must be between 0 and 20.")
        return val
    
class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].required = True