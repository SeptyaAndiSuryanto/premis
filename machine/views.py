from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

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


class CategoryDetail(DetailView):
    """Detail view for PartCategory."""

    model = PartCategory
    context_object_name = 'category'
    queryset = PartCategory.objects.all().prefetch_related('children')
    template_name = 'part/category.html'

    def get_context_data(self, **kwargs):
        """Returns custom context data for the CategoryDetail view:

        - part_count: Number of parts in this category
        - starred_directly: True if this category is starred directly by the requesting user
        - starred: True if this category is starred by the requesting user
        """
        context = super().get_context_data(**kwargs).copy()

        try:
            context['part_count'] = kwargs['object'].partcount()
        except KeyError:
            context['part_count'] = 0

        # Get current category
        category = kwargs.get('object', None)

        if category:

            # Insert "starred" information
            context['starred_directly'] = category.is_starred_by(
                self.request.user,
                include_parents=False,
            )

            if context['starred_directly']:
                # Save a database lookup - if 'starred_directly' is True, we know 'starred' is also
                context['starred'] = True
            else:
                context['starred'] = category.is_starred_by(self.request.user)

        return context


class MachineCategoryData(ServerSideDatatableView):
    queryset = MachineCategory.objects.filter(parent=None)
    columns = ['name', 'description', 'pathstring']