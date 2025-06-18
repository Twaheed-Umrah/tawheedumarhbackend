from rest_framework import serializers
from .models import Booking
from packages.serializers import PackageListSerializer
from packages.models import Package

class BookingSerializer(serializers.ModelSerializer):
    package_details = PackageListSerializer(source='package', read_only=True)
    booking_id = serializers.UUIDField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    # Make package optional since frontend might not send package ID
    package = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'package', 'package_details', 'name', 'email', 'phone',
            'package_type', 'travel_month', 'nights', 'passengers', 
            'departure_date', 'special_requirements', 'total_amount', 
            'status', 'status_display'
        ]
        read_only_fields = ['user', 'booking_id', 'status_display']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        # Try to find matching package based on package_type if no package ID provided
        if not validated_data.get('package') and validated_data.get('package_type'):
            try:
                package = Package.objects.filter(
                    package_type__icontains=validated_data['package_type']
                ).first()
                if package:
                    validated_data['package'] = package
            except Package.DoesNotExist:
                pass
        
        # Calculate total amount if package is available
        if validated_data.get('package') and validated_data.get('passengers'):
            package = validated_data['package']
            passengers = validated_data['passengers']
            validated_data['total_amount'] = package.effective_price * passengers
        
        return super().create(validated_data)

    def validate(self, data):
        # Ensure required fields from frontend are present
        required_fields = ['name', 'email', 'phone', 'package_type', 'travel_month', 'nights', 'passengers']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} is required")
        
        # Validate email format
        if data.get('email') and '@' not in data['email']:
            raise serializers.ValidationError("Invalid email format")
        
        # Validate positive numbers
        if data.get('nights') and data['nights'] <= 0:
            raise serializers.ValidationError("Nights must be a positive number")
        
        if data.get('passengers') and data['passengers'] <= 0:
            raise serializers.ValidationError("Passengers must be a positive number")
        
        return data

class BookingTrackingSerializer(serializers.ModelSerializer):
    package_details = PackageListSerializer(source='package', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'package_details', 'name', 'email', 'phone',
            'package_type', 'travel_month', 'nights', 'passengers',
            'departure_date', 'total_amount', 'status', 
            'status_display', 'created_at', 'updated_at'
        ]

class BookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing bookings"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'name', 'package_type', 'travel_month', 
            'nights', 'passengers', 'total_amount', 'status',
            'status_display', 'created_at'
        ]  

class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = ['status', 'status_display']
    
    # Override validate method to remove the parent validation
    def validate(self, data):
        # Only validate status field
        if 'status' in data:
            valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
            if data['status'] not in valid_statuses:
                raise serializers.ValidationError("Invalid status value")
        return data