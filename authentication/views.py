# views.py
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .models import CustomUser, UserActivity
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    UserActivitySerializer,
    ChangePasswordSerializer
)

# Custom permission classes
class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superadmin

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin

# Utility function to log user activities
def log_user_activity(user, action, description="", ip_address=None):
    UserActivity.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=ip_address
    )

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        # Log activity
        ip_address = request.META.get('REMOTE_ADDR')
        log_user_activity(user, 'USER_REGISTERED', f'New user registered with role: {user.role}', ip_address)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        
        # Log activity
        ip_address = request.META.get('REMOTE_ADDR')
        log_user_activity(user, 'USER_LOGIN', 'User logged in', ip_address)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        })

class LogoutView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Debug: Print user info
            print(f"User: {request.user}")
            print(f"Is authenticated: {request.user.is_authenticated}")
            
            # Delete the user's token
            request.user.auth_token.delete()
            
            # Log activity
            ip_address = request.META.get('REMOTE_ADDR')
            log_user_activity(request.user, 'USER_LOGOUT', 'User logged out', ip_address)
            
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Logout error: {e}")  # Debug: Print error
            return Response({
                'error': 'An error occurred during logout'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Rest of your views remain the same but add csrf_exempt decorator for POST/PUT/DELETE endpoints
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """List all users - Admin only"""
    serializer_class = UserListSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return CustomUser.objects.all().order_by('-created_at')
        elif user.is_admin:
            return CustomUser.objects.exclude(role='superadmin').order_by('-created_at')
        return CustomUser.objects.none()

class AllUsersView(generics.ListAPIView):
    """Get all users - Available to all authenticated users"""
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return all active users, ordered by creation date
        return CustomUser.objects.filter(is_active=True).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Log activity
        log_user_activity(
            request.user, 
            'USERS_VIEWED', 
            'User viewed all users list',
            request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'users': serializer.data,
            'count': queryset.count(),
            'message': 'Users retrieved successfully'
        })

@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update, delete specific user - Admin only"""
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superadmin:
            return CustomUser.objects.all()
        elif user.is_admin:
            return CustomUser.objects.exclude(role='superadmin')
        return CustomUser.objects.none()
    
    def perform_update(self, serializer):
        user = serializer.save()
        log_user_activity(
            self.request.user, 
            'USER_UPDATED', 
            f'Updated user: {user.username}',
            self.request.META.get('REMOTE_ADDR')
        )
    
    def perform_destroy(self, instance):
        log_user_activity(
            self.request.user, 
            'USER_DELETED', 
            f'Deleted user: {instance.username}',
            self.request.META.get('REMOTE_ADDR')
        )
        instance.delete()

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    """Create new user - Admin only"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        log_user_activity(
            request.user, 
            'USER_CREATED', 
            f'Created user: {user.username} with role: {user.role}',
            request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(generics.UpdateAPIView):
    """Change user password"""
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        log_user_activity(
            user, 
            'PASSWORD_CHANGED', 
            'User changed password',
            request.META.get('REMOTE_ADDR')
        )
        
        return Response({'message': 'Password changed successfully'})

class UserActivityView(generics.ListAPIView):
    """View user activities - Admin only"""
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            return UserActivity.objects.filter(user_id=user_id).order_by('-timestamp')
        return UserActivity.objects.all().order_by('-timestamp')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """
    Get all users - Function-based view available to all authenticated users
    Returns basic user information for all active users
    """
    try:
        # Get all active users
        users = CustomUser.objects.filter(is_active=True).order_by('-created_at')
        
        # Serialize the data
        serializer = UserListSerializer(users, many=True)
        
        # Log activity
        log_user_activity(
            request.user, 
            'ALL_USERS_ACCESSED', 
            'User accessed all users list via function',
            request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'success': True,
            'users': serializer.data,
            'total_users': users.count(),
            'message': 'All users retrieved successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': 'Failed to retrieve users',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminOrSuperAdmin])
@csrf_exempt
def toggle_user_status(request, user_id):
    """Activate/Deactivate user"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent non-superadmin from modifying superadmin accounts
    if user.is_superadmin and not request.user.is_superadmin:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    user.is_active = not user.is_active
    user.save()
    
    action = 'USER_ACTIVATED' if user.is_active else 'USER_DEACTIVATED'
    log_user_activity(
        request.user, 
        action, 
        f'User {user.username} {"activated" if user.is_active else "deactivated"}',
        request.META.get('REMOTE_ADDR')
    )
    
    return Response({
        'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
        'is_active': user.is_active
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """Get current user's permissions"""
    user = request.user
    permissions_data = {
        'role': user.role,
        'role_display': user.get_role_display(),
        'permissions': {
            'can_manage_users': user.can_manage_users(),
            'is_superadmin': user.is_superadmin,
            'is_admin': user.is_admin,
            'is_consulting': user.is_consulting,
            'is_seouser': user.is_seouser,
            'can_create_roles': {
                'superadmin': user.can_create_role('superadmin'),
                'admin': user.can_create_role('admin'),
                'consulting': user.can_create_role('consulting'),
                'seouser': user.can_create_role('seouser'),
                'user': user.can_create_role('user'),
            }
        }
    }
    return Response(permissions_data)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify if the provided token is valid and return user information
    """
    try:
        # If we reach here, the token is valid (IsAuthenticated permission passed)
        user = request.user
        
        # Log activity
        log_user_activity(
            user, 
            'TOKEN_VERIFIED', 
            'User token verified successfully',
            request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'valid': True,
            'user': UserProfileSerializer(user).data,
            'message': 'Token is valid'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'valid': False,
            'error': 'Token verification failed',
            'message': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)