from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import UserProfile

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Handle goals first
        if "save-goals" in request.POST:
            # normalize commas to dots for EU keyboards
            raw_water = (request.POST.get("water_goal") or "").replace(",", ".")
            raw_sleep = (request.POST.get("sleep_goal") or "").replace(",", ".")

            try:
                if raw_water != "":
                    val = float(raw_water)
                    profile.water_goal = round(max(0.0, min(20.0, val)), 1)
            except ValueError:
                pass

            try:
                if raw_sleep != "":
                    val = float(raw_sleep)
                    profile.sleep_goal = round(max(0.0, min(20.0, val)), 1)
            except ValueError:
                pass

            profile.save()
            messages.success(request, "Goals updated.")
            return redirect("profiles:profile")

        # Then handle description
        if "description" in request.POST:
            profile.description = (request.POST.get("description") or "")[:500]
            profile.save()
            messages.success(request, "Description updated.")
            return redirect("profiles:profile")

    return render(request, "profiles/my_profile.html", {
        "username": request.user.username,
        "description": profile.description,
        "water_intake": profile.water_intake,
        "sleep_hours": profile.sleep_hours,
        "water_goal": profile.water_goal,
        "sleep_goal": profile.sleep_goal,
        "member_since": request.user.date_joined,
    })

def populate_profile_on_signup(request, user, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=user)

    raw_water = (request.POST.get("water_goal") or "").replace(",", ".")
    raw_sleep = (request.POST.get("sleep_goal") or "").replace(",", ".")

    try:
        profile.water_goal = round(max(0.0, min(20.0, float(raw_water))), 1) if raw_water else 8.0
    except ValueError:
        profile.water_goal = 8.0

    try:
        profile.sleep_goal = round(max(0.0, min(20.0, float(raw_sleep))), 1) if raw_sleep else 8.0
    except ValueError:
        profile.sleep_goal = 8.0

    profile.save()

def update_water_sleep(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        raw_water = (request.POST.get('water') or "").replace(",", ".")
        if raw_water.strip():
            try:
                val = float(raw_water)
                profile.water_intake = round(max(0.0, min(20.0, val)), 1)
            except ValueError:
                pass

        raw_sleep = (request.POST.get('sleep') or "").replace(",", ".")
        if raw_sleep.strip():
            try:
                val = float(raw_sleep)
                profile.sleep_hours = round(max(0.0, min(20.0, val)), 1)
            except ValueError:
                pass

        profile.save()
        return redirect('tracker:overview')