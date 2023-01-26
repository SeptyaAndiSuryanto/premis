from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView


from .models import MachineCategory, Machine

from django_serverside_datatable.views import ServerSideDatatableView


# Create your views here.
class Category(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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

    model = MachineCategory
    context_object_name = 'category'
    queryset = MachineCategory.objects.all().prefetch_related('children')
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        """Returns custom context data for the CategoryDetail view:

        - machine_count: Number of parts in this category
        - starred_directly: True if this category is starred directly by the requesting user
        - starred: True if this category is starred by the requesting user
        """
        context = super().get_context_data(**kwargs).copy()

        try:
            context['machine_count'] = kwargs['object'].machine_count()
        except KeyError:
            context['machine_count'] = 0

        # Get current category
        # category = kwargs.get('object', None)

        # if category:

        #     # Insert "starred" information
        #     context['starred_directly'] = category.is_starred_by(
        #         self.request.user,
        #         include_parents=False,
        #     )

        #     if context['starred_directly']:
        #         # Save a database lookup - if 'starred_directly' is True, we know 'starred' is also
        #         context['starred'] = True
        #     else:
        #         context['starred'] = category.is_starred_by(self.request.user)

        return context


class MachineCategoryData(ServerSideDatatableView):
    model = MachineCategory
    # queryset = MachineCategory.objects.filter(parent=None)
    columns = ['id','name', 'description', 'pathstring']
    

    # def get_ajax_url(self):
    #     if self.kwargs.get('pk'):
    #         return reverse(self.request.resolver_match.url_name, kwargs={'pk':self.kwargs['pk']})
    #     return reverse(self.request.resolver_match.url_name)

    def get_queryset(self):
        queryset = MachineCategory.objects.filter(parent=None)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        """Returns custom context data for the MachineCategory view:

        - machine_count: Number of parts in this category
        """
        context = super().get_context_data(**kwargs).copy()

        try:
            context['machine_count'] = kwargs['object'].machine_count()
        except KeyError:
            context['machine_count'] = 0
        return context


