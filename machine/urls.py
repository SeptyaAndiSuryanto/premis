from django.urls import path
from .views import MachineIndex, MachineCategoryData

urlpatterns = [
    path("", MachineIndex.as_view(), name="machine-index"),
    path('data/', MachineCategoryData.as_view()), 

]