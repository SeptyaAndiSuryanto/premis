from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView

from premis.views import IndexView
from users.views import PremisLoginView, PremisLogout


urlpatterns = [
    path('', login_required(IndexView.as_view(), login_url='login'), name="index"),
    path("login/", PremisLoginView.as_view(), name="login"),
    path("logout/", PremisLogout.as_view(), name="logout"),
    path('admin/', admin.site.urls),
    path('machine/', include('machine.urls')),
]
