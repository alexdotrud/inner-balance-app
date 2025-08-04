from django.urls import path
from .views import DashboardView, TaskListView

app_name = 'tracker'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('tasks/', TaskListView.as_view(), name='task_list'),  
]