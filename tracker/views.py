from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
            try:
                task.save()
                # Counts created tasks, after 5 shows a seccess message
                task_count = Task.objects.filter(user=request.user).count()
                if task_count == 5:
                    messages.success(request, "You’ve created 5 daily tasks. Now you can start your tracking journey together with INNNER BALANCE")

            except IntegrityError:
                messages.error(request, "You already have a task with this title.")

        return redirect('tracker:dashboard')

class TaskListView(ListView):
    model = Task
    template_name = 'tracker/tasks.html'

class TaskUpdateView(SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'tracker/task_form.html'
    success_message = 'Task updated!'
    
    #obly the author can edit his tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tracker:dashboard')
    

class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tracker/task_confirm_delete.html'
    success_message = 'Task Deleted!'

    #obly the author can edit his tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)