from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "dashboard.html"
