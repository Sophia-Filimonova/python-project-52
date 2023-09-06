from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


class UserLoginView(LoginView):
    template_name = 'form.html'
    form_class = AuthenticationForm
    next_page = reverse_lazy('home')
    extra_context = {
        'header': _('Login'),
        'button_text': _('Enter'),
    }

    def form_valid(self, form):
        messages.success(self.request, _('You are logged in'))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       _('Please enter a correct username and password. \
                         Note that both fields may be case-sensitive.'))
        return super().form_invalid(form)


class UserLogoutView(LogoutView):

    def get(self, request):
        logout(request)
        messages.info(request, _('You are logged out'))
        return redirect('home')
