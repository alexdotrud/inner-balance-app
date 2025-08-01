from django.shortcuts import render
from django.http import HttpResponse
from .models import Tasks

# Create your views here.
def my_tracker(request):
    user_tasks = Tasks.objects.filter(user_id=request.user)
    context = {
        'tasks': user_tasks,
    }
    return render(request, 'tracker/my_tracker.html', context)