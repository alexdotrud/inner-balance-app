from django.views.generic import TemplateView, ListView
from .models import Task


class DashboardView(TemplateView):
    template_name = 'tracker/dashboard.html'

class TaskListView(ListView):
    model = Task
    template_name = 'tracker/tasks.html'

