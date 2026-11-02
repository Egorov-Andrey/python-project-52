from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/label.html"
    context_object_name = 'labels'
    login_url = 'login'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels')
    success_message = "Статус успешно создан"
    login_url = 'login'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels')
    success_message = "Статус успешно изменён"
    login_url = 'login'


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    login_url = 'login'
    
    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, "Невозможно удалить метку")
            return redirect('labels')
        
        messages.success(self.request, "Метка успешна удалён")
        return super().form_valid(form)





