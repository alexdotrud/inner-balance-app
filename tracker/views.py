from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tracker/dashboard.html'
    
    # Sending data to template
    def get_context_data(self, **kwargs):
        tasks = Task.objects.filter(user=self.request.user)
        return {
            'tasks': tasks,
            'task_count': tasks.count(),
            'task_form': TaskForm(),
        }
    # If form submitted -redirects to dashboard.
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
        return redirect('tracker:dashboard')

class TaskListView(ListView):
    model = Task
    template_name = 'tracker/tasks.html'

