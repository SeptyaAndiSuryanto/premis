from django.shortcuts import render
from django_filters import rest_framework as filters

from .models import Task


# Create your views here.
class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = '__all__'