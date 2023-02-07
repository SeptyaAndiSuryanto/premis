from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include
from . import views
from .views import Category, MachineCategoryData, MachineCategoryList


category_urls = [
    # re_path(r'(?P<pk>\d+)/', views.CategoryDetail.as_view(), name='category-detail')
    # re_path(r'(?P<pk>\d+)/', include([
    #     # re_path(r'^delete/', views.CategoryDelete.as_view(), name='category-delete'),
    #     # Anything else
    #     re_path(r'^.*$', views.CategoryDetail.as_view(), name='category-detail'),
        path('api/machinecategory/', MachineCategoryList.as_view(), name='machine-category-list'),
        path('api/machinecategory/<int:id>', MachineCategoryList.as_view(), name='machine-category-list'),
        path('data/', MachineCategoryData.as_view(), name="machine-category-data"), 
        # path('data/<int:pk>/', MachineCategoryData.as_view(), name="machine-subcategory-data"), 
        path('', Category.as_view(), name="machine-category"),
    ]

api_urls = [
]

machinepatterns = [
    # re_path(r'^.*$', MachineIndex.as_view(), name='machine-index'),
    # path('category/', Category.as_view(), name="machine-category"),
    
    re_path(r'^api/', include(api_urls)),
    re_path(r'^category/', include(category_urls)),
]

