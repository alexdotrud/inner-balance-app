from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()
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

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.description = (request.POST.get("description") or "")[:500]

        water = request.POST.get("water_goal")
        sleep = request.POST.get("sleep_goal")
        try:
            if water not in (None, ""):
                profile.water_goal = max(0, min(20, int(water)))
        except ValueError:
            pass
        try:
            if sleep not in (None, ""):
                profile.sleep_goal = max(0.0, min(20.0, float(sleep)))
        except ValueError:
            pass

        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("tracker:profile")

    return render(request, "tracker/my_profile.html", {
        "username": request.user.username,
        "description": profile.description,
        "water_intake": profile.water_intake,
        "sleep_hours": profile.sleep_hours,
        "water_goal": profile.water_goal,
        "sleep_goal": profile.sleep_goal,
    })