from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class UserForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=150, required=True, label=_("First name")
    )
    last_name = forms.CharField(
        max_length=150, required=True, label=_("Last name")
    )

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2'
                  ]
