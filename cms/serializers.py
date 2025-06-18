# serializers.py
from rest_framework import serializers
from .models import HeroSection, Component, Package, HomePage
from authentication.permissions import IsAdminOrSuperAdmin, IsSuperAdmin
import base64
import uuid
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image uploads through base64 strings.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            if 'base64,' in data:
                header, data = data.split('base64,')
                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    self.fail('invalid_image')

                # Use Pillow to get image format
                image = Image.open(BytesIO(decoded_file))
                file_extension = image.format.lower()

                file_name = f"{uuid.uuid4().hex[:12]}.{file_extension}"
                data = ContentFile(decoded_file, name=file_name)

        return super().to_internal_value(data)


class Base64VideoField(serializers.FileField):
    """
    A Django REST framework field for handling video uploads through base64 strings.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:video'):
            if 'base64,' in data:
                header, data = data.split('base64,')
                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    raise serializers.ValidationError("Invalid video file")

                # Extract video format from header
                # e.g., "data:video/mp4;base64," -> "mp4"
                if 'video/' in header:
                    file_extension = header.split('video/')[1].split(';')[0]
                else:
                    file_extension = 'mp4'  # default extension

                file_name = f"{uuid.uuid4().hex[:12]}.{file_extension}"
                data = ContentFile(decoded_file, name=file_name)

        return super().to_internal_value(data)


class HeroSectionSerializer(serializers.ModelSerializer):
    background_image = Base64ImageField(max_length=None, use_url=True, required=False)
    background_video = Base64VideoField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'subtitle', 'background_video', 
            'background_image', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Override to ensure proper URL representation for video files
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        if instance.background_video and request:
            data['background_video'] = request.build_absolute_uri(instance.background_video.url)
        
        return data


class ComponentSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Component
        fields = [
            'id', 'name', 'component_type', 'title', 'description', 
            'image', 'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PackageSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Package
        fields = [
            'id', 'package_type', 'title', 'description', 'price', 
            'currency', 'duration_days', 'image', 'features', 
            'is_active', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PackageUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = Package
        fields = [
            'title', 'description', 'price', 'currency', 'duration_days', 
            'image', 'features', 'is_active', 'is_featured'
        ]


class HomePageSerializer(serializers.ModelSerializer):
    background_image = Base64ImageField(max_length=None, use_url=True, required=False)
    background_video = Base64VideoField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = HomePage
        fields = [
            'id', 'welcome_title', 'welcome_subtitle', 'content', 
            'background_video', 'background_image', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Override to ensure proper URL representation for both image and video files
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Build absolute URL for background_video
        if instance.background_video and request:
            data['background_video'] = request.build_absolute_uri(instance.background_video.url)
        
        # Build absolute URL for background_image (THIS WAS MISSING!)
        if instance.background_image and request:
            data['background_image'] = request.build_absolute_uri(instance.background_image.url)
        
        return data


class HomePageUpdateSerializer(serializers.ModelSerializer):
    background_image = Base64ImageField(max_length=None, use_url=True, required=False)
    background_video = Base64VideoField(max_length=None, use_url=True, required=False)
    
    class Meta:
        model = HomePage
        fields = [
            'welcome_title', 'welcome_subtitle', 'content', 
            'background_video', 'background_image', 'is_active'
        ]

    def to_representation(self, instance):
        """
        Override to ensure proper URL representation for both image and video files
        """
        data = super().to_representation(instance)
        request = self.context.get('request')
        
        # Build absolute URL for background_video
        if instance.background_video and request:
            data['background_video'] = request.build_absolute_uri(instance.background_video.url)
            
        # Build absolute URL for background_image (THIS WAS MISSING!)
        if instance.background_image and request:
            data['background_image'] = request.build_absolute_uri(instance.background_image.url)
        
        return data