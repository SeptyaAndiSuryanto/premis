from rest_framework import generics
from rest_framework.response import Response

from task.models import Task, Period, CheckItem
from task.serializers import TaskSerializer, PeriodSerializer, CheckItemSerializer
from task.views import TaskFilter, PeriodFilter, CheckItemFilter


class TaskApi(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter

    # def get(self, request, format=None):
    #     if 'id' in request.GET:
    #         id = request.GET['id']
    #         queryset = self.queryset.filter(parent__id=id)
    #     else:
    #         queryset = self.queryset.filter(parent__isnull=True)

    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response({
    #         'draw': 1,
    #         'recordsTotal': self.queryset.count(),
    #         'recordsFiltered': queryset.count(),
    #         'data': serializer.data,
    #     })


class PeriodApi(generics.ListAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    filter_class = PeriodFilter


class CheckItemApi(generics.ListAPIView):
    queryset = CheckItem.objects.all()
    serializer_class = CheckItemSerializer
    filter_class = CheckItemFilter
    
# class MachineCategoryCreateApi(generics.CreateAPIView):
#     queryset = MachineCategory.objects.all()
#     serializer_class = MachineCategorySerializer


# class MachineCategoryUpdateApi(generics.RetrieveUpdateAPIView):
#     queryset = MachineCategory.objects.all()
#     serializer_class = MachineCategorySerializer


# class MachineCategoryDeleteApi(generics.DestroyAPIView):
#     queryset = MachineCategory.objects.all()
#     serializer_class = MachineCategorySerializer