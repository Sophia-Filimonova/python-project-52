from django_filters import FilterSet, ModelChoiceFilter, BooleanFilter
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Task
from task_manager.users.models import MyUser
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskFilter(FilterSet):

    status = ModelChoiceFilter(
        label=_('Status'),
        queryset=Status.objects.all(),
    )

    executor = ModelChoiceFilter(
        label=_('Executor'),
        queryset=MyUser.objects.all(),
    )

    labels = ModelChoiceFilter(
        label=_('Label'),
        queryset=Label.objects.all(),
    )

    your_tasks = BooleanFilter(
        label=_('Only your tasks'),
        widget=forms.CheckboxInput,
        method='get_your_tasks',
    )

    def get_your_tasks(self, queryset, field_name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = []
