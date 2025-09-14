from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', views.user_update, name='user_update'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    
    # Password Management
    path('change-password/', views.change_password, name='change_password'),
    path('users/<int:user_id>/change-password/', views.change_password, name='admin_change_password'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Role and Permissions
    path('role-permissions/', views.role_permissions, name='role_permissions'),
]