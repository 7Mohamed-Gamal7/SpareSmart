from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    """Extended User model with additional fields"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('sales', 'Sales Representative'),
        ('cashier', 'Cashier'),
        ('viewer', 'Viewer Only'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active_employee = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'

class UserProfile(models.Model):
    """Additional profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=17, blank=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Permission(models.Model):
    """Custom permissions for the application"""
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'custom_permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

class RolePermission(models.Model):
    """Mapping between roles and permissions"""
    role = models.CharField(max_length=20)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.role} - {self.permission.name}"
    
    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'