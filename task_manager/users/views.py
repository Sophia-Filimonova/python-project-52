# from django.urls import reverse_lazy
from django.views.generic import ListView
#    # CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
# from django.contrib.messages.views import SuccessMessageMixin

# from task_manager.mixins import AuthRequiredMixin,\
#     UserPermissionMixin, DeleteProtectionMixin
from .models import MyUser as User
# from .forms import UserForm


class UserListView(ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = 'users'
    extra_context = {
        'header': _('Users'),
    }
