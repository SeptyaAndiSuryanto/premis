from rest_framework import generics
from rest_framework.response import Response
from .serializers import MachineCategorySerializer, MachineSerializer
from .models import MachineCategory, Machine
from .views import MachineCategoryFilter

from task.models import Task
from task.serializers import TaskSerializer
from task.views import TaskFilter



class MachineCategoryApi(generics.ListAPIView):
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


class MachineApi(generics.ListAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    filter_class = MachineCategoryFilter

    def get(self, request, format=None):
        if 'id' in request.GET:
            id = request.GET['id']
            queryset = self.queryset.filter(category_id=id)
        else:
            queryset = self.queryset.filter(category_id=None)

        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'draw': 1,
            'recordsTotal': self.queryset.count(),
            'recordsFiltered': queryset.count(),
            'data': serializer.data,
        })
    

class ItemRelated(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter

    def get(self, request, format=None):
        if 'id' in request.GET:
            id = request.GET['id']
            queryset = self.queryset.filter(machine=id)
        else:
            queryset = self.queryset.filter(machine=None)

        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'draw': 1,
            'recordsTotal': self.queryset.count(),
            'recordsFiltered': queryset.count(),
            'data': serializer.data,
        })
    


class MachineCategoryListApi(generics.ListAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer
    filter_class = MachineCategoryFilter

    def get(self, request, format=None):
        if 'id' in request.GET:
            id = request.GET['id']
            queryset = self.queryset.filter(parent__id=id)
        else:
            queryset = self.queryset.all()

        serializer = self.serializer_class(queryset, many=True)
        return Response({
            'draw': 1,
            'recordsTotal': self.queryset.count(),
            'recordsFiltered': queryset.count(),
            'data': serializer.data,
        })


class MachineCategoryCreateApi(generics.CreateAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer


class MachineCategoryUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer


class MachineCategoryDeleteApi(generics.DestroyAPIView):
    queryset = MachineCategory.objects.all()
    serializer_class = MachineCategorySerializer