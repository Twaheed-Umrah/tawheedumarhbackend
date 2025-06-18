from rest_framework import serializers
from .models import Package

class PackageSerializer(serializers.ModelSerializer):
    effective_price = serializers.ReadOnlyField()
    package_type_display = serializers.CharField(source='get_package_type_display', read_only=True)

    class Meta:
        model = Package
        fields = '__all__'

class PackageListSerializer(serializers.ModelSerializer):
    effective_price = serializers.ReadOnlyField()
    package_type_display = serializers.CharField(source='get_package_type_display', read_only=True)

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'package_type', 'package_type_display', 
            'short_description', 'price', 'discounted_price', 
            'effective_price', 'duration_days', 'image', 'is_featured'
        ]