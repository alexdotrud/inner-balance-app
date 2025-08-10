from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import UserProfile

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
        return redirect("profiles:profile")

    return render(request, "profiles/my_profile.html", {
        "username": request.user.username,
        "description": profile.description,
        "water_intake": profile.water_intake,
        "sleep_hours": profile.sleep_hours,
        "water_goal": profile.water_goal,
        "sleep_goal": profile.sleep_goal,
    })

def populate_profile_on_signup(request, user, **kwargs):
    water_goal = request.POST.get("water_goal")
    sleep_goal = request.POST.get("sleep_goal")

    profile, _ = UserProfile.objects.get_or_create(user=user)
    if water_goal:
        profile.water_goal = int(water_goal)
    if sleep_goal:
        profile.sleep_goal = float(sleep_goal)
    profile.save()

def update_water_sleep(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        water_value = request.POST.get('water')
        if water_value and water_value.strip():
            try:
                profile.water_intake = int(water_value)
            except ValueError:
                pass

        sleep_value = request.POST.get('sleep')
        if sleep_value and sleep_value.strip():
            try:
                sleep_hours = float(sleep_value)
                profile.sleep_hours = min(sleep_hours, 20.0)
            except ValueError:
                pass

        profile.save()
        return redirect('tracker:overview')