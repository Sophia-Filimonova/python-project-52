from django.contrib.auth.forms import BaseUserCreationForm, UserCreationForm

from .models import MyUser


class UserCreateForm(UserCreationForm):

    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields['last_name'].required = True
        self.fields['first_name'].requred = True

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name',
                  'username', 'password1', 'password2'
                  ]


class UserUpdateForm(BaseUserCreationForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
