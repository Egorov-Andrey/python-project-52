from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, UpdateView

from .forms import CustomLoginForm, CustomUserCreationForm, CustomUserUpdateForm

# Create your views here.


class CustomLoginView(SuccessMessageMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'users/login.html'
    success_message = "Вы залогинены"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')

    def form_valid(self, form):
        print(">>> CustomLoginView.form_valid вызван!")  # ← добавь это
        return super().form_valid(form)


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Вы разлогинены"
    next_page = reverse_lazy('login')


def create_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.info(request, "Пользователь успешно зарегистрирован")
            return redirect('main')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


class CustomUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_message = "Пользователь успешно изменен"

    def get_success_url(self):
        return reverse_lazy('main')


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):

    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = "Пользователь успешно удалён"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_to_delete'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):

        user_to_delete = self.get_object()
        
        if request.user == user_to_delete:
            messages.error(request, "Вы не можете удалить самого себя")
            return redirect('users')
        
        return super().delete(request, *args, **kwargs)


class UserListView(LoginRequiredMixin, ListView):

    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    login_url = 'login'
