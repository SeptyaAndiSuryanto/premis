from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response

from .models import MachineCategory, Machine
from .serializers import MachineCategorySerializer

from django_serverside_datatable.views import ServerSideDatatableView



# Create your views here.
class MachineCategoryFilter(filters.FilterSet):
    class Meta:
        model = MachineCategory
        fields = '__all__'


class MachineCategoryList(generics.ListAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer
    filter_class = MachineCategoryFilter

    def get(self, request, format=None):
        if 'id' in request.GET:
            id = request.GET['id']
            queryset = self.queryset.filter(parent__id=id)
        else:
            queryset = self.queryset.filter(parent__isnull=True)

        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'draw': 1,
            'recordsTotal': self.queryset.count(),
            'recordsFiltered': queryset.count(),
            'data': serializer.data,
        })
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response({
    #         "draw": 1,
    #         "recordsTotal": self.queryset.count(),
    #         "recordsFiltered": queryset.count(),
    #         "data": serializer.data
    #     })

class Category(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "category.html"
    # model = MachineCategory
    # context_object_name = "machine_categ ory"

    # def get_queryset(self):
    #     return MachineCategory.objects.all()
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the PartIndex view:

        - children: Number of child categories
        - category_count: Number of child categories
        - machine_count: Number of machine contained
        """
        context = super().get_context_data(**kwargs).copy()

        if 'id' in self.request.GET:
            id = self.request.GET['id']
            print(id)
            children = MachineCategory.objects.get(id=id)
            context['children'] = children
            context['category_count'] = MachineCategory.objects.count()
            context['machine_count'] = Machine.objects.filter(category=id).count()

        else:
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
    columns = ['id','name', 'description', 'pathstring']

    # queryset = MachineCategory.objects.filter(parent=None)
    
    def get_queryset(self, **kwargs):
        print(self.request.GET)
        parent_id = self.request.GET.get('pk')
        if parent_id:
            queryset = queryset.filter(parent__id=parent_id)
        else:
            queryset = MachineCategory.objects.filter(parent=None)
        print(queryset)
        return queryset

    # def get_datatable_options(self):
    #     options = super().get_datatable_options()
    #     options['start'] = int(self.request.GET.get('start', 0))
    #     options['length'] = int(self.request.GET.get('length', 10))
    #     return options


