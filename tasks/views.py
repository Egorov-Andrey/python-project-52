from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import TaskForm
from .models import Label, Status, Task

User = get_user_model()


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    login_url = 'login'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        status_id = self.request.GET.get('status')
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        executor_id = self.request.GET.get('executor')
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        
        label_id = self.request.GET.get('label')
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        
        if self.request.GET.get('own_tasks'):
            queryset = queryset.filter(author=self.request.user)
        
        return queryset.select_related('status', 'author', 'executor')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    login_url = 'login'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно создана"
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/form.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно изменена"
    login_url = 'login'


class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')
    success_message = "Задача успешно удалена"
    login_url = 'login'