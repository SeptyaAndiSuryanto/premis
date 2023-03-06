from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from . import views, api
from .views import MachineCategoryView, MachineCategoryList, MachineCategoryCreateAPIView, MachineCategoryCreateView
# MachineCategoryData


category_urls = [
    path('api/machinecategory/list', api.MachineCategoryListApi.as_view(), name='machine-category-list-all'),
    path('api/machinecategory/', api.MachineCategoryApi.as_view(), name='machine-category-list'),
    path('api/machinecategory/?id=<int:id>', api.MachineCategoryApi.as_view(), name='machine-category-list'),
    path('api/machinecategory/create', api.MachineCategoryCreateApi.as_view(), name='api-machine-category-create'),
    path('api/machinecategory/<int:pk>/update/', api.MachineCategoryUpdateApi.as_view(), name='machine-category-update'),
    path('api/machinecategory/<int:pk>/delete', api.MachineCategoryDeleteApi.as_view(), name='machine-category-delete'),

    path('', MachineCategoryView.as_view(), name="machine-category"),
    path('machinecategory/create', MachineCategoryCreateView.as_view(), name='machine-category-create'),
    path('<int:id>', MachineCategoryView.as_view(), name="machine-category"),
    ]

api_urls = [
]

machinepatterns = [
    # re_path(r'^.*$', MachineIndex.as_view(), name='machine-index'),
    # path('category/', Category.as_view(), name="machine-category"),
    
    re_path(r'^api/', include(api_urls)),
    re_path(r'^category/', include(category_urls)),
]

