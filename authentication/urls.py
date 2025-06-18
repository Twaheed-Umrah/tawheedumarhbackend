# urls.py
from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    UserDetailView,
    CreateUserView,
    ChangePasswordView,
    UserActivityView,
    LogoutView,
    toggle_user_status,
    user_permissions,
    get_all_users,
    verify_token
)

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
   path('logout/', LogoutView.as_view(), name='user-logout'), 
   path('verify/', verify_token, name='verify_token'),

    # Profile management
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('permissions/', user_permissions, name='user-permissions'),
    
    # Admin user management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', CreateUserView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/toggle-status/', toggle_user_status, name='toggle-user-status'),
    
    # Activity tracking
    path('activities/', UserActivityView.as_view(), name='user-activities'),
    path('users/<int:user_id>/activities/', UserActivityView.as_view(), name='user-specific-activities'),
    path('users/get-all/', get_all_users, name='get-all-users'),

]