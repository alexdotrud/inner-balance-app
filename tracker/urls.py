from . import views
from django.urls import path


urlpatterns = [
    path('', views.TasksList.as_view(), name='home'),
]