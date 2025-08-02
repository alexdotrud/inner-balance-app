from django.shortcuts import render
from django.views import generic
from .models import Task

# Create your views here.
class TasksList(generic.ListView):
    model = Task
    context_object_name = 'tasks'