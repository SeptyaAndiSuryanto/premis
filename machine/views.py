from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, CreateView
from django.shortcuts import render
from django.urls import reverse_lazy, resolve

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .forms import MachineCategoryForm
from .models import MachineCategory, Machine
from .serializers import MachineCategorySerializer

# from django_serverside_datatable.views import ServerSideDatatableView



class MachineCategoryFilter(filters.FilterSet):
    class Meta:
        model = MachineCategory
        fields = '__all__'


class MachineFilter(filters.FilterSet):
    class Meta:
        model = Machine
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
    

class MachineCategoryView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "category.html"
    
    def get_context_data(self, **kwargs):
        """Returns custom context data for the PartIndex view:

        - children: Number of child categories
        - category_count: Number of child categories
        - machine_count: Number of machine contained
        """
        context = super().get_context_data(**kwargs).copy()

        if 'id' in self.request.GET:
            id = self.request.GET['id']
            children = MachineCategory.objects.get(id=id)
            context['path'] = children.pathstring
            context['desc'] = children.description
            context['category_count'] = children.get_descendants().count()
            context['machine_count'] = Machine.objects.filter(category=id).count()

        else:
            # View top-level categories
            children = MachineCategory.objects.filter(parent=None)
            context['path'] = ""
            context['desc'] = "Top level machine category"
            context['category_count'] = children.get_descendants().count()
            context['machine_count'] = Machine.objects.count()
        
        return context


class MachineCategoryCreateAPIView(generics.CreateAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer
    # template_name = 'category_create_modal.html'
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.is_ajax():
            if response.status_code == 201:
                return render(request, 'yourmodel_create_success.html')
            else:
                return render(request, 'machine-category-create.html', {'form': self.get_serializer().data}, status=400)
        # serializer = MachineCategorySerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=400)
    

class MachineCategoryCreateView(CreateView):
    model = MachineCategory
    form_class = MachineCategoryForm
    template_name = "category_create_modal.html"
    success_url = reverse_lazy('machine-category')

    def get_default_parent(request):
        # Get the id from the request URL
        id = resolve(request.path_info).kwargs.get('id')
        print(id)

        # Use the id to get the parent object
        parent = MachineCategory.objects.filter(id=id).first()

        # Return the parent object or default to root node if it doesn't exist
        return parent

    def form_valid(self, form):
        # Get the parent object using the request object
        parent = self.get_default_parent(self.request)
        print(parent)
        print("parent")
        # Set the parent field of the PremisTree instance
        form.instance.parent = parent

        # Call the parent class's form_valid() method to save the form
        return super().form_valid(form)
    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return render(request, 'category_create_success.html')
    #     else:
    #         return render(request, self.template_name, {'form':form}, status=400)


class MachineView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "machine.html"

    def get_context_data(self, **kwargs):
        """Returns custom context data for the PartIndex view:

        - children: Number of child categories
        - category_count: Number of child categories
        - machine_count: Number of machine contained
        """
        context = super().get_context_data(**kwargs).copy()

        if 'id' in self.request.GET:
            id = self.request.GET['id']
            machine = Machine.objects.get(id=id)
            context['breadcrumbs'] = machine.category.pathstring
            context['desc'] = machine.description
            context['name'] = machine.name
            context['IPN'] = machine.IPN
            context['category'] = machine.category.name
        
        return context
    

'''
# class CategoryDetail(DetailView):
#     """Detail view for PartCategory."""

#     model = MachineCategory
#     context_object_name = 'category'
#     queryset = MachineCategory.objects.all().prefetch_related('children')
#     template_name = 'category.html'

#     def get_context_data(self, **kwargs):
#         """Returns custom context data for the CategoryDetail view:

#         - machine_count: Number of parts in this category
#         - starred_directly: True if this category is starred directly by the requesting user
#         - starred: True if this category is starred by the requesting user
#         """
#         context = super().get_context_data(**kwargs).copy()

#         try:
#             context['machine_count'] = kwargs['object'].machine_count()
#         except KeyError:
#             context['machine_count'] = 0

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

        # return context


# class MachineCategoryData(ServerSideDatatableView):
#     model = MachineCategory
#     columns = ['id','name', 'description', 'pathstring']

#     # queryset = MachineCategory.objects.filter(parent=None)
    
#     def get_queryset(self, **kwargs):
#         print(self.request.GET)
#         parent_id = self.request.GET.get('pk')
#         if parent_id:
#             queryset = queryset.filter(parent__id=parent_id)
#         else:
#             queryset = MachineCategory.objects.filter(parent=None)
#         return queryset

    # def get_datatable_options(self):
    #     options = super().get_datatable_options()
    #     options['start'] = int(self.request.GET.get('start', 0))
    #     options['length'] = int(self.request.GET.get('length', 10))
    #     return options



'''
