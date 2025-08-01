from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def my_tracker(request):

    return render(request, 'tracker/my_tracker.html')