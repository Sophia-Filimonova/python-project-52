from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home')
    success_message = _('You are logged in')
    extra_context = {
        'header': _('Login'),
        'button_text': _('Enter'),
    }


class UserLogoutView(LogoutView):

    def get(self, request):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('home')