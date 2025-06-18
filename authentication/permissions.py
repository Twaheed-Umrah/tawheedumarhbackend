# permissions.py
from rest_framework import permissions

class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins and superadmins to access.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_superadmin)  # Check BOTH fields
        )

class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superadmin

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow users to access their own data or admins to access any data.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for owner or admin
        if request.method in permissions.SAFE_METHODS:
            return (
                obj == request.user or 
                request.user.is_admin or 
                request.user.is_superadmin
            )
        
        # Write permissions for owner or admin
        return (
            obj == request.user or 
            request.user.is_admin or 
            request.user.is_superadmin
        )

class IsConsultingOrAbove(permissions.BasePermission):
    """
    Custom permission for consulting level and above.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_consulting

class IsSEOUserOrAbove(permissions.BasePermission):
    """
    Custom permission for SEO user level and above.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seouser

class CanManageRole(permissions.BasePermission):
    """
    Custom permission to check if user can manage specific roles.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user is trying to create/modify a role
        target_role = request.data.get('role') if hasattr(request, 'data') else None
        if target_role:
            return request.user.can_create_role(target_role)
        
        return True