from rest_framework import serializers
from .models import Task, CheckItem, Period



class CheckItemSerializer(serializers.ModelSerializer):
    period = serializers.CharField(source='period.name', read_only=True)
    class Meta:
        model = CheckItem
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    machine = serializers.CharField(source='machine.name', read_only=True)
    item = serializers.CharField(source='item.name', read_only=True)
    period = serializers.CharField(source='item.period', read_only=True)
    creation_user = serializers.CharField(source='creation_user.username', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        # fields = ('id','machine','item','description','creation_date','creation_user')


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'