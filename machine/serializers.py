from rest_framework import serializers
from .models import MachineCategory

class MachineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCategory
        fields = '__all__'