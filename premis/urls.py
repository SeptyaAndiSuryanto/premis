from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.conf.urls import include

from premis.views import IndexView
from users.views import PremisLoginView, PremisLogout
from machine.urls import machinepatterns as machine_urls
from task.urls import taskpatterns as task_urls


authurls = [
    re_path(r'^login/', PremisLoginView.as_view(), name="login"),
    re_path(r'^logout/', PremisLogout.as_view(), name="logout"),
]

fronturls = [
    path('', login_required(IndexView.as_view(), login_url='login'), name="index"),
    re_path(r'^machine/', include(machine_urls)),
    re_path(r'^task/', include(task_urls)),
]

backurls = []

urlpatterns = [
    re_path('', include(authurls)),
    path('', include(fronturls)),
    re_path('', include(backurls)),
    path('admin/', admin.site.urls),
]
