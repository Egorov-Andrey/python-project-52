from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses/status.html"
    context_object_name = 'statuses'
    login_url = 'login'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно создан"
    login_url = 'login'


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses')
    success_message = "Статус успешно изменён"
    login_url = 'login'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    login_url = 'login'
    
    def form_valid(self, form):

        status = self.get_object()
        if status.tasks.exists():
            messages.error(self.request, "Невозможно удалить статус")
            return redirect('statuses')
        
        messages.success(self.request, "Статус успешно удалён")
        return super().form_valid(form)


