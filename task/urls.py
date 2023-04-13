from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from . import api, views

api_urls = [
    path('task/list', api.TaskApi.as_view(), name='task-list'),
    path('period/list', api.PeriodApi.as_view(), name='period-list'),
    path('checkitem/list', api.CheckItemApi.as_view(), name='checkitem-list')
]

task_urls = [
    path('', views.TaskView.as_view(), name="task"),
    # path('machinecategory/create', MachineCategoryCreateView.as_view(), name='machine-category-create'),
    # path('<int:id>', MachineCategoryView.as_view(), name="machine-category"),
]

taskpatterns = [
    re_path(r'', include(task_urls)),
    re_path(r'^api/', include(api_urls)),
]

