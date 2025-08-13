from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm
from profiles.models import UserProfile
from django.core.exceptions import ValidationError


class OverviewView(LoginRequiredMixin, TemplateView):
    """
    Shows daily overview, resets counters if needed, and handles quick task creation.
    """
    template_name = 'tracker/overview.html'
    
    # Sending data to template
    def get_context_data(self, **kwargs):
        profile = reset_tasks_if_needed(self.request.user)
        tasks = Task.objects.filter(user=self.request.user)
        return {
            'tasks': tasks,
            'task_count': tasks.count(),
            'task_form': TaskForm(),
            'water_count': profile.water_intake,
            'water_goal': profile.water_goal,
            'sleep_count': profile.sleep_hours,
            'sleep_goal': profile.sleep_goal,
        }
    
    # If form submitted -redirects to overview.
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            try:
                task.save()
                # Counts created tasks, after 5 shows a seccess message
                task_count = Task.objects.filter(user=request.user).count()


            except IntegrityError:
                messages.error(request, "You already have a task with this title.")

        return redirect('tracker:overview')
    

def add_task(request):
    """
    Handles separate task creation form page (GET shows form, POST saves task).
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'add_task.html', {'task_form': form})


def update_water_sleep(request):
    """
    Updates current day's water intake and sleep hours for the logged-in user.
    """
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        
        raw_water = (request.POST.get("water") or "").replace(",", ".")
        raw_sleep = (request.POST.get("sleep") or "").replace(",", ".")
    
        try:
            if raw_water.strip():
                profile.water_intake = float(raw_water)
            if raw_sleep.strip():
                profile.sleep_hours = float(raw_sleep)

            profile.full_clean()
            profile.save()
            messages.success(request, "Progress updated.")
        except (ValueError, ValidationError):
            messages.error(request, "Invalid intake value. Please check the limits.")


        profile.save()
        return redirect('tracker:overview')
    

def reset_tasks_if_needed(user):
    """
    Resets all tasks and counters if the date has changed since last reset. Once per day.
    """
    today = timezone.now().date()

    # creating new database row with reset data
    profile, created = UserProfile.objects.get_or_create(user=user)

    if profile.last_reset != today:
        Task.objects.filter(user=user).update(is_completed=False)
        profile.last_reset = today
        profile.water_intake = 0
        profile.sleep_hours = 0.0
        profile.save()
        
    return profile
    

def update_tasks(request):
    """
    Marks tasks as completed/incomplete based on submitted checkboxes.
    """
    if request.method == 'POST':
        tasks = Task.objects.filter(user=request.user)
        checked_ids = {int(key.split('_')[1]) for key in request.POST if key.startswith('task_')}

        for task in tasks:
            task.is_completed = task.id in checked_ids
            task.save()

    return redirect('tracker:overview')


class TaskListView(ListView):
    model = Task
    template_name = 'tracker/tasks.html'


class TaskCreateView(SuccessMessageMixin, CreateView):
    """
    Creates a new task for the logged-in user.
    """
    model = Task
    fields = ['title', 'description']
    template_name = 'tracker/task_form.html'
    success_message = 'Task added!'

  #set the user before saving
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tracker:overview')



class TaskUpdateView(SuccessMessageMixin, UpdateView):
    """
    Updates an existing task owned by the logged-in user.
    """
    model = Task
    fields = ['title', 'description']
    template_name = 'tracker/task_form.html'
    success_message = 'Task updated!'
    
    #obly the author can edit his tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tracker:overview')
    

class TaskDeleteView(SuccessMessageMixin, DeleteView):
    """
    Deletes an existing task owned by the logged-in user.
    """
    model = Task
    template_name = 'tracker/task_confirm_delete.html'
    success_url = reverse_lazy('tracker:overview')
    success_message = 'Task Deleted!'

    #obly the author can edit his tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
