from django.urls import path
from . import views
from .views import OverviewView, TaskListView, TaskDeleteView, TaskUpdateView, TaskCreateView

app_name = 'tracker'

urlpatterns = [
    path('overview', OverviewView.as_view(), name='overview'),
    path('tasks/', TaskListView.as_view(), name='task_list'),  
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('update-tasks/', views.update_tasks, name='update_tasks'),
    path('update-water-sleep/', views.update_water_sleep, name='update_water_sleep'), 
]
