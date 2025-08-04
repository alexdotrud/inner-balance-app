from django.urls import path
from .views import DashboardView, TaskListView

app_name = 'tracker'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
]