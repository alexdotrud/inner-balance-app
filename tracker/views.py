from django.shortcuts import render
from django.views import generic
from .models import Task

# Dashboard view 
def dashboard(request):
    return render(request, 'tracker/index.html')

# Tasks list page using Django's generic ListView
class TasksList(generic.ListView):
    model = Task
    context_object_name = 'tasks'  # use 'tasks' in your template
    template_name = 'tracker/task_list.html'  # optional if following naming convention