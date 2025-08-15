from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import UserProfile
from django.core.exceptions import ValidationError
from .forms import ProfileAvatarForm

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
                if raw_water.strip():
                    profile.water_goal = float(raw_water)
                if raw_sleep.strip():
                    profile.sleep_goal = float(raw_sleep)

                profile.full_clean()
                profile.save()
                messages.success(request, "Goals updated.")
            except (ValueError, ValidationError):
                messages.error(request, "Goal should not be less than 1 or more than 20.")
            return redirect("profiles:profile")

        # Then handle description
        if "description" in request.POST:
            profile.description = (request.POST.get("description") or "")[:500]
            profile.save()
            messages.success(request, "Description updated.")
            return redirect("profiles:profile")

    return render(request, "profiles/my_profile.html", {
        "profile": profile,
        "username": request.user.username,
        "description": profile.description,
        "water_intake": profile.water_intake,
        "sleep_hours": profile.sleep_hours,
        "water_goal": profile.water_goal,
        "sleep_goal": profile.sleep_goal,
        "member_since": request.user.date_joined,
    })

@login_required
def profile_avatar_view(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Avatar updated.")
        else:
            messages.error(request, "Invalid image. Check file size/type.")
    return redirect("profiles:profile")

def populate_profile_on_signup(request, user, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=user)

    raw_water = (request.POST.get("water_goal") or "").replace(",", ".")
    raw_sleep = (request.POST.get("sleep_goal") or "").replace(",", ".")
    try:
        profile.water_goal = float(raw_water) if raw_water else 8.0
        profile.sleep_goal = float(raw_sleep) if raw_sleep else 8.0
        profile.full_clean()
    except (ValueError, ValidationError):
        profile.water_goal = 8.0
        profile.sleep_goal = 8.0

    profile.save()

def update_water_sleep(request):
    if request.method == 'POST':
          profile, _ = UserProfile.objects.get_or_create(user=request.user)

          raw_water = (request.POST.get('water') or "").replace(",", ".")
          raw_sleep = (request.POST.get('sleep') or "").replace(",", ".")
    try:
        if raw_water.strip():
                profile.water_intake = float(raw_water)
        if raw_sleep.strip():
                profile.sleep_hours = float(raw_sleep)

        profile.full_clean()
        profile.save()
        messages.success(request, "Progress updated.")
    except (ValueError, ValidationError):
        messages.error(request, "Invalid intake value. Please check the limits.")

    return redirect('tracker:overview')