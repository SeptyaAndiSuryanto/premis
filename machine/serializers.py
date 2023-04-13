from rest_framework import serializers
from .models import MachineCategory, Machine

class MachineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCategory
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Machine
        fields = '__all__'

    def to_representation(self, instance):
        my_fields = {'IPN', 'active', 'category__name', 'creation_date', 'description', 'id', 'name'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = "-"
            except KeyError:
                pass
        return data

    # def create(self, validated_data):
    #     # Create and return a new MyModel instance using the validated data
    #     return MachineCategory.objects.create(**validated_data)


class MachineCategoryFormSerializer(serializers.Serializer):
    parent = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()