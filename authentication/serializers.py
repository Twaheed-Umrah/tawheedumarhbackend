# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserActivity

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLES, default='user')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'password', 'role')

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_role(self, value):
        """Validate if the requesting user can create users with this role"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if not request.user.can_create_role(value):
                raise serializers.ValidationError(
                    f"You don't have permission to create users with role: {value}"
                )
        return value

    def create(self, validated_data):
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        # Create username from email
        username = validated_data['email'].split('@')[0]

        # Ensure username is unique
        original_username = username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', 'user'),
            first_name=first_name,
            last_name=last_name
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user_obj = CustomUser.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
                
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'name', 'email', 'phone', 'date_of_birth', 
            'address', 'is_verified', 'role', 'role_display',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'is_verified', 'created_at', 'updated_at')
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (admin view)"""
    name = serializers.SerializerMethodField()
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name', 'name', 'email', 'phone', 'role', 
            'role_display', 'is_active', 'is_verified', 'created_at'
        )
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'address',
            'role'
        )

    def validate_role(self, value):
        """Validate role changes"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            if not request.user.can_create_role(value):
                raise serializers.ValidationError(
                    f"You don't have permission to assign role: {value}"
                )
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ('id', 'user', 'user_name', 'action', 'description', 'ip_address', 'timestamp')
        read_only_fields = ('id', 'timestamp')

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value