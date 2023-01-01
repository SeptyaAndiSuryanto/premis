from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import MachineCategory, Machine

from django_serverside_datatable.views import ServerSideDatatableView


# Create your views here.
class Category(ListView):
    template_name = "category.html"
    model = Machine
    context_object_name = "machine"

    def get_queryset(self):
        return Machine.objects.all().select_related('category')
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the PartIndex view:

        - children: Number of child categories
        - category_count: Number of child categories
        - part_count: Number of parts contained
        """
        context = super().get_context_data(**kwargs).copy()

        # View top-level categories
        children = MachineCategory.objects.filter(parent=None)

        context['children'] = children
        context['category_count'] = MachineCategory.objects.count()
        context['machine_count'] = Machine.objects.count()

        return context
    

class MachineCategoryData(ServerSideDatatableView):
    queryset = MachineCategory.objects.filter(parent=None)
    columns = ['name', 'description', 'pathstring']