from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import MyLoginRequiredMixin,\
     UserPermissionMixin, DeleteProtectionMixin
from .models import MyUser as User
from .forms import UserForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = 'users'
    extra_context = {
        'header': _('Users'),
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'header': _('Registration'),
        'button_text': _('Register '),
    }
    success_message = _('User is created successfully')


class UserUpdateView(MyLoginRequiredMixin, UserPermissionMixin,
                     SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users')
    success_message = _('User is successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button_text': _('Update'),
    }


class UserDeleteView(MyLoginRequiredMixin, UserPermissionMixin,
                     DeleteProtectionMixin,
                     SuccessMessageMixin, DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('users')
    success_message = _('User is successfully deleted')
    extra_context = {
        'header': _('Deleting user'),
        'button_text': _('Yes, delete'),
    }
