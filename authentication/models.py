# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = [
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('consulting', 'Consulting'),
        ('seouser', 'SEO User'),
        ('user', 'User'),
    ]
    
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Role-based permissions
    @property
    def is_superadmin(self):
        return self.role == 'superadmin'
    
    @property
    def is_admin(self):
        return self.role in ['superadmin', 'admin']
    
    @property
    def is_consulting(self):
        return self.role in ['superadmin', 'admin', 'consulting']
    
    @property
    def is_seouser(self):
        return self.role in ['superadmin', 'admin', 'consulting', 'seouser']
    
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role in ['superadmin', 'admin']
    
    def can_create_role(self, target_role):
        """Check if user can create users with specific role"""
        role_hierarchy = {
            'superadmin': ['superadmin', 'admin', 'consulting', 'seouser', 'user'],
            'admin': ['admin', 'consulting', 'seouser', 'user'],
            'consulting': ['user'],
            'seouser': [],
            'user': []
        }
        return target_role in role_hierarchy.get(self.role, [])

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class UserActivity(models.Model):
    """Track user activities for audit purposes"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"