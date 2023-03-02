from rest_framework import serializers
from .models import MachineCategory

class MachineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCategory
        fields = '__all__'

    def create(self, validated_data):
        # Create and return a new MyModel instance using the validated data
        return MachineCategory.objects.create(**validated_data)