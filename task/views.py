from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, View, CreateView

from django_filters import rest_framework as filters

from .models import Task, Period, CheckItem, Record


# Create your views here.
class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = '__all__'


class PeriodFilter(filters.FilterSet):
    class Meta:
        model = Period
        fields = '__all__'


class CheckItemFilter(filters.FilterSet):
    class Meta:
        model = CheckItem
        fields = '__all__'

class TaskView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "task.html"