from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from . import views, api
from .views import MachineCategoryView, MachineCategoryList, MachineCategoryCreateAPIView, MachineCategoryCreateView, MachineView
# MachineCategoryData


category_urls = [
    path('', MachineCategoryView.as_view(), name="machine-category"),
    path('machinecategory/create', MachineCategoryCreateView.as_view(), name='machine-category-create'),
    path('<int:id>', MachineCategoryView.as_view(), name="machine-category"),
]

machine_urls = [
    path('', MachineView.as_view(), name="machine"),

]

api_urls = [
    path('machinecategory/list', api.MachineCategoryListApi.as_view(), name='machine-category-list-all'),
    path('machinecategory/', api.MachineCategoryApi.as_view(), name='machine-category-list'),
    path('machinecategory/?id=<int:id>', api.MachineCategoryApi.as_view(), name='machine-category-list'),
    path('machinecategory/create', api.MachineCategoryCreateApi.as_view(), name='api-machine-category-create'),
    path('machinecategory/<int:pk>/update/', api.MachineCategoryUpdateApi.as_view(), name='machine-category-update'),
    path('machinecategory/<int:pk>/delete', api.MachineCategoryDeleteApi.as_view(), name='machine-category-delete'),
    path('machine/?id=<int:id>', api.MachineApi.as_view(), name='machine-list'),
    path('machine/', api.MachineApi.as_view(), name='machine-list'),
    path('machine/taskrelated/?id=<int:id>', api.ItemRelated.as_view(), name='task-related'),
    path('machine/taskrelated/', api.ItemRelated.as_view(), name='task-related'),
]

machinepatterns = [
    # re_path(r'^.*$', MachineIndex.as_view(), name='machine-index'),
    # path('category/', Category.as_view(), name="machine-category"),
    
    re_path(r'^api/', include(api_urls)),
    re_path(r'^category/', include(category_urls)),
    re_path(r'', include(machine_urls)),
]

