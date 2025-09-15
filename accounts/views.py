from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from .models import User, UserProfile, Permission, RolePermission
from .forms import (
    CustomLoginForm, UserCreationForm, UserUpdateForm, 
    UserProfileForm, PasswordChangeForm, RolePermissionForm
)
from dashboard.models import ActivityLog
import json

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active and user.is_active_employee:
                    login(request, user)
                    
                    # Set session expiry based on remember_me
                    if not remember_me:
                        request.session.set_expiry(0)  # Browser session
                    else:
                        request.session.set_expiry(86400 * 30)  # 30 days
                    
                    # Log the login activity
                    ActivityLog.objects.create(
                        user=user,
                        action='login',
                        description=f'User {user.username} logged in',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                    
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    
                    # Redirect to next page or dashboard
                    next_page = request.GET.get('next', 'dashboard:home')
                    return redirect(next_page)
                else:
                    messages.error(request, 'Your account is inactive. Please contact the administrator.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    """User logout view"""
    user = request.user
    
    # Log the logout activity
    ActivityLog.objects.create(
        user=user,
        action='logout',
        description=f'User {user.username} logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'manager'])
def user_list(request):
    """List all users with pagination and filtering"""
    users = User.objects.all().order_by('-created_at')
    
    # Filtering
    role_filter = request.GET.get('role')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    if status_filter == 'active':
        users = users.filter(is_active=True, is_active_employee=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'suspended':
        users = users.filter(is_active_employee=False)
    
    if search_query:
        users = users.filter(
            models.Q(username__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'role_choices': User.ROLE_CHOICES,
        'current_filters': {
            'role': role_filter,
            'status': status_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'accounts/user_list.html', context)

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'manager'])
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user = user_form.save()
                    
                    # Create user profile
                    if profile_form.cleaned_data:
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()
                    
                    # Log the activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='create',
                        description=f'Created new user: {user.username}',
                        content_object=user,
                        ip_address=get_client_ip(request)
                    )
                    
                    messages.success(request, f'User {user.username} created successfully.')
                    return redirect('accounts:user_detail', user_id=user.id)
                    
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
    else:
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'Create New User'
    }
    
    return render(request, 'accounts/user_form.html', context)

@login_required
def user_detail(request, user_id):
    """View user details"""
    user = get_object_or_404(User, id=user_id)
    
    # Check permissions
    if not (request.user.is_superuser or request.user.role in ['admin', 'manager'] or request.user == user):
        messages.error(request, 'You do not have permission to view this user.')
        return redirect('dashboard:home')
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    # Get recent activities
    recent_activities = user.activity_logs.all()[:10]
    
    context = {
        'user_obj': user,
        'profile': profile,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/user_detail.html', context)

@login_required
def user_update(request, user_id):
    """Update user information"""
    user = get_object_or_404(User, id=user_id)
    
    # Check permissions
    if not (request.user.role in ['admin', 'manager'] or request.user == user):
        messages.error(request, 'You do not have permission to edit this user.')
        return redirect('accounts:user_detail', user_id=user.id)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            try:
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                    
                    # Log the activity
                    ActivityLog.objects.create(
                        user=request.user,
                        action='update',
                        description=f'Updated user: {user.username}',
                        content_object=user,
                        ip_address=get_client_ip(request)
                    )
                    
                    messages.success(request, 'User information updated successfully.')
                    return redirect('accounts:user_detail', user_id=user.id)
                    
            except Exception as e:
                messages.error(request, f'Error updating user: {str(e)}')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user,
        'title': f'Edit User: {user.username}'
    }
    
    return render(request, 'accounts/user_form.html', context)

@login_required
def change_password(request, user_id=None):
    """Change user password"""
    if user_id and request.user.role in ['admin', 'manager']:
        user = get_object_or_404(User, id=user_id)
        is_admin_changing = True
    else:
        user = request.user
        is_admin_changing = False
    
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST, is_admin_changing=is_admin_changing)
        
        if form.is_valid():
            form.save()
            
            # Log the activity
            ActivityLog.objects.create(
                user=request.user,
                action='update',
                description=f'Changed password for user: {user.username}',
                content_object=user,
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Password changed successfully.')
            
            if is_admin_changing:
                return redirect('accounts:user_detail', user_id=user.id)
            else:
                return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(user, is_admin_changing=is_admin_changing)
    
    context = {
        'form': form,
        'user_obj': user,
        'is_admin_changing': is_admin_changing,
    }
    
    return render(request, 'accounts/change_password.html', context)

@login_required
def profile(request):
    """User profile view"""
    return render(request, 'accounts/profile.html')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.role == 'admin')
def role_permissions(request):
    """Manage role permissions"""
    if request.method == 'POST':
        form = RolePermissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role permissions updated successfully.')
            return redirect('accounts:role_permissions')
    else:
        form = RolePermissionForm()
    
    # Get current role permissions
    role_permissions = {}
    for role, _ in User.ROLE_CHOICES:
        role_permissions[role] = RolePermission.objects.filter(role=role)
    
    context = {
        'form': form,
        'role_permissions': role_permissions,
        'role_choices': User.ROLE_CHOICES,
        'permissions': Permission.objects.all(),
    }
    
    return render(request, 'accounts/role_permissions.html', context)

@login_required
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """Toggle user active status via AJAX"""
    if not request.user.role in ['admin', 'manager']:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent self-deactivation
    if user == request.user:
        return JsonResponse({'success': False, 'error': 'Cannot deactivate your own account'})
    
    user.is_active_employee = not user.is_active_employee
    user.save()
    
    # Log the activity
    action_desc = 'activated' if user.is_active_employee else 'deactivated'
    ActivityLog.objects.create(
        user=request.user,
        action='update',
        description=f'{action_desc.capitalize()} user: {user.username}',
        content_object=user,
        ip_address=get_client_ip(request)
    )
    
    return JsonResponse({
        'success': True,
        'status': user.is_active_employee,
        'message': f'User {action_desc} successfully'
    })

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Utility function to check if user is admin
def is_admin_user(user):
    """Check if user is superuser or admin"""
    return user.is_superuser or user.role == 'admin'

# Utility function to check if user is admin or manager
def is_admin_or_manager(user):
    """Check if user is superuser, admin, or manager"""
    return user.is_superuser or user.role in ['admin', 'manager']

# Utility function to check user permissions
def has_permission(user, permission_codename):
    """Check if user has specific permission"""
    # Superuser has all permissions
    if user.is_superuser:
        return True

    # Admin role has all permissions
    if user.role == 'admin':
        return True

    return RolePermission.objects.filter(
        role=user.role,
        permission__codename=permission_codename
    ).exists()

# Decorator for permission checking
def permission_required(permission_codename):
    """Decorator to check user permission"""
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not has_permission(request.user, permission_codename):
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard:home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator