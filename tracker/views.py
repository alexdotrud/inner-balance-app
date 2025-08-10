from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import redirect, render
from django import forms
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task, DailyReset, UserProfile
from .forms import TaskForm



class OverviewView(LoginRequiredMixin, TemplateView):
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
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title and len(title) <= 50 and len(description) <= 200:
            Task.objects.create(user=request.user, title=title, description=description)
            return redirect("tracker:overview")
        else:
            messages.error(request, "Title (max 50 chars) and description (max 200 chars) are required.")

    return render(request, "tracker/add_task.html")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["description", "water_goal", "sleep_goal"]

    def clean_water_goal(self):
        val = self.cleaned_data.get("water_goal")
        if val is None or val < 0 or val > 20:
            raise forms.ValidationError("Water goal must be between 0 and 20.")
        return val

    def clean_sleep_goal(self):
        val = self.cleaned_data.get("sleep_goal")
        if val is None or val < 0 or val > 20:
            raise forms.ValidationError("Sleep goal must be between 0 and 20.")
        return val

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.description = (request.POST.get("description") or "")[:500]

        water = request.POST.get("water_goal")
        sleep = request.POST.get("sleep_goal")
        try:
            if water not in (None, ""):
                profile.water_goal = max(0, min(20, int(water)))
        except ValueError:
            pass
        try:
            if sleep not in (None, ""):
                profile.sleep_goal = max(0.0, min(20.0, float(sleep)))
        except ValueError:
            pass

        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("tracker:profile")

    return render(request, "tracker/my_profile.html", {
        "username": request.user.username,
        "description": profile.description,
        "water_intake": profile.water_intake,
        "sleep_hours": profile.sleep_hours,
        "water_goal": profile.water_goal,
        "sleep_goal": profile.sleep_goal,
    })

def populate_profile_on_signup(request, user, **kwargs):
    water_goal = request.POST.get("water_goal")
    sleep_goal = request.POST.get("sleep_goal")

    profile, _ = UserProfile.objects.get_or_create(user=user)
    if water_goal:
        profile.water_goal = int(water_goal)
    if sleep_goal:
        profile.sleep_goal = float(sleep_goal)
    profile.save()



def update_water_sleep(request):
    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        
        water_value = request.POST.get('water')
        if water_value and water_value.strip():
            try:
                profile.water_intake = int(water_value)
            except ValueError:
                pass

        sleep_value = request.POST.get('sleep')
        if sleep_value and sleep_value.strip():
            try:
                sleep_hours = float(sleep_value)
                profile.sleep_hours = min(sleep_hours, 20.0)  # Cap at 20
            except ValueError:
                pass 

        profile.save()
        return redirect('tracker:overview')
    

def reset_tasks_if_needed(user):
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
    model = Task
    fields = ['title', 'description']
    template_name = 'tracker/task_form.html'

  #set the user before saving
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tracker:overview')



class TaskUpdateView(SuccessMessageMixin, UpdateView):
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
    model = Task
    template_name = 'tracker/task_confirm_delete.html'
    success_url = reverse_lazy('tracker:overview')
    success_message = 'Task Deleted!'

    #obly the author can edit his tasks
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
