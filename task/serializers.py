from rest_framework import serializers
from .models import Task, CheckItem
from machine.models import Machine
from machine import serializers as machine_serializers


class CheckItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckItem
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    machine_name = machine_serializers.MachineSerializer(source='machine.name', read_only=True)
    item_name = CheckItemSerializer(source='item.name', read_only=True)

    class Meta:
        model = Task
        fields = ('id','machine_name','item_name')
