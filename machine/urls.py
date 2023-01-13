from django.urls import path, re_path, include
from . import views
from .views import Category, MachineCategoryData


category_urls = [
    # re_path(r'(?P<pk>\d+)/', views.CategoryDetail.as_view(), name='category-detail')
    re_path(r'(?P<pk>\d+)/', include([
        # re_path(r'^delete/', views.CategoryDelete.as_view(), name='category-delete'),
        # Anything else
        re_path(r'^.*$', views.CategoryDetail.as_view(), name='category-detail'),
    ]))
]

urlpatterns = [
    # re_path(r'^.*$', MachineIndex.as_view(), name='machine-index'),
    path("category/", Category.as_view(), name="machine-category"),
    path('data/', MachineCategoryData.as_view()), 
    re_path(r'^category/', include(category_urls)),


]

