from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("profile/avatar/", views.profile_avatar_view, name="profile_avatar"),
]
