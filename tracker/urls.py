from django.urls import path
from .views import dashboard, TasksList

urlpatterns = [
    path('', dashboard, name='dashboard'),  # homepage
]