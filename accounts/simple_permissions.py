
# نظام الصلاحيات المبسط لـ SpareSmart

def user_has_permission(user, permission_name):
    """
    فحص صلاحيات المستخدم
    """
    # المستخدم Superuser لديه جميع الصلاحيات
    if user.is_superuser:
        return True
    
    # المدير لديه جميع الصلاحيات
    if user.role == 'admin':
        return True
    
    # صلاحيات حسب الدور
    role_permissions = {
        'manager': [
            'view_products', 'add_products', 'change_products',
            'view_sales', 'add_sales', 'change_sales',
            'view_purchases', 'add_purchases', 'change_purchases',
            'view_expenses', 'add_expenses', 'change_expenses',
            'process_payments', 'view_reports', 'generate_reports'
        ],
        'sales': [
            'view_products', 'view_sales', 'add_sales', 'change_sales',
            'process_payments', 'view_reports'
        ],
        'cashier': [
            'view_products', 'view_sales', 'add_sales', 'process_payments'
        ],
        'viewer': [
            'view_products', 'view_sales', 'view_purchases', 
            'view_expenses', 'view_reports'
        ]
    }
    
    user_permissions = role_permissions.get(user.role, [])
    return permission_name in user_permissions

def user_can_access_admin_features(user):
    """فحص إمكانية الوصول للميزات الإدارية"""
    return user.is_superuser or user.role in ['admin', 'manager']

def user_can_manage_users(user):
    """فحص إمكانية إدارة المستخدمين"""
    return user.is_superuser or user.role == 'admin'
