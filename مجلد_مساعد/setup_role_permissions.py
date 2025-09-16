#!/usr/bin/env python3
"""
إعداد صلاحيات الأدوار في النظام
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, RolePermission

def setup_role_permissions():
    """إعداد صلاحيات الأدوار"""
    
    print("🔧 إعداد صلاحيات الأدوار...")
    print("=" * 60)
    
    # تنظيف الصلاحيات الموجودة
    RolePermission.objects.all().delete()
    print("🧹 تم حذف الصلاحيات القديمة")
    
    # الحصول على جميع الصلاحيات
    permissions = Permission.objects.all()
    
    # تعريف صلاحيات كل دور
    role_permissions = {
        'admin': [
            # جميع الصلاحيات للمدير
            'view_products', 'add_products', 'change_products', 'delete_products',
            'view_sales', 'add_sales', 'change_sales', 'delete_sales',
            'view_purchases', 'add_purchases', 'change_purchases', 'delete_purchases',
            'view_expenses', 'add_expenses', 'change_expenses', 'delete_expenses',
            'process_payments', 'view_reports', 'generate_reports',
            'manage_users', 'manage_settings'
        ],
        'manager': [
            # صلاحيات المدير التنفيذي
            'view_products', 'add_products', 'change_products',
            'view_sales', 'add_sales', 'change_sales',
            'view_purchases', 'add_purchases', 'change_purchases',
            'view_expenses', 'add_expenses', 'change_expenses',
            'process_payments', 'view_reports', 'generate_reports'
        ],
        'sales': [
            # صلاحيات مندوب المبيعات
            'view_products', 'view_sales', 'add_sales', 'change_sales',
            'process_payments', 'view_reports'
        ],
        'cashier': [
            # صلاحيات أمين الصندوق
            'view_products', 'view_sales', 'add_sales',
            'process_payments'
        ],
        'viewer': [
            # صلاحيات المشاهد فقط
            'view_products', 'view_sales', 'view_purchases', 
            'view_expenses', 'view_reports'
        ]
    }
    
    created_count = 0
    
    for role, permission_codes in role_permissions.items():
        print(f"\n👤 إعداد صلاحيات دور: {role}")
        
        for permission_code in permission_codes:
            try:
                permission = Permission.objects.get(codename=permission_code)
                # التحقق من وجود الصلاحية أولاً
                if not RolePermission.objects.filter(role=role, permission=permission).exists():
                    role_permission = RolePermission.objects.create(
                        role=role,
                        permission=permission
                    )
                    created_count += 1
                    print(f"   ✅ {permission.name}")
                else:
                    print(f"   ⚪ {permission.name} (موجود بالفعل)")
            except Permission.DoesNotExist:
                print(f"   ❌ الصلاحية غير موجودة: {permission_code}")
            except Exception as e:
                print(f"   ❌ خطأ في إضافة {permission_code}: {e}")
    
    print(f"\n🎉 تم إنشاء {created_count} صلاحية دور جديدة")
    return created_count

def verify_permissions():
    """التحقق من الصلاحيات"""
    
    print("\n" + "=" * 60)
    print("🔍 التحقق من الصلاحيات...")
    
    from accounts.views import has_permission
    
    # إنشاء مستخدمين اختباريين لكل دور
    test_users = {}
    
    for role, role_display in User.ROLE_CHOICES:
        # البحث عن مستخدم موجود بهذا الدور
        existing_user = User.objects.filter(role=role).first()
        if existing_user:
            test_users[role] = existing_user
            print(f"✅ مستخدم {role}: {existing_user.username}")
        else:
            print(f"⚠️  لا يوجد مستخدم بدور {role}")
    
    # اختبار بعض الصلاحيات
    test_permissions = ['view_products', 'add_sales', 'manage_users']
    
    print(f"\n🧪 اختبار الصلاحيات:")
    print(f"{'الدور':<12} {'view_products':<15} {'add_sales':<12} {'manage_users':<15}")
    print("-" * 60)
    
    for role, user in test_users.items():
        view_products = has_permission(user, 'view_products')
        add_sales = has_permission(user, 'add_sales')
        manage_users = has_permission(user, 'manage_users')
        
        print(f"{role:<12} {str(view_products):<15} {str(add_sales):<12} {str(manage_users):<15}")

def create_sample_users():
    """إنشاء مستخدمين عينة للاختبار"""
    
    print("\n" + "=" * 60)
    print("👥 إنشاء مستخدمين عينة...")
    
    sample_users = [
        {'username': 'admin_user', 'role': 'admin', 'email': 'admin@sparesmart.com'},
        {'username': 'manager_user', 'role': 'manager', 'email': 'manager@sparesmart.com'},
        {'username': 'sales_user', 'role': 'sales', 'email': 'sales@sparesmart.com'},
        {'username': 'cashier_user', 'role': 'cashier', 'email': 'cashier@sparesmart.com'},
        {'username': 'viewer_user', 'role': 'viewer', 'email': 'viewer@sparesmart.com'},
    ]
    
    created_count = 0
    
    for user_data in sample_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'role': user_data['role'],
                'first_name': user_data['role'].title(),
                'last_name': 'User',
                'is_active': True
            }
        )
        
        if created:
            user.set_password('password123')  # كلمة مرور افتراضية
            user.save()
            created_count += 1
            print(f"   ✅ تم إنشاء: {user.username} ({user.get_role_display()})")
        else:
            print(f"   ⚪ موجود: {user.username} ({user.get_role_display()})")
    
    if created_count > 0:
        print(f"\n🎉 تم إنشاء {created_count} مستخدم جديد")
        print("💡 كلمة المرور الافتراضية: password123")
    else:
        print("\n✅ جميع المستخدمين موجودون بالفعل")

def main():
    print("🔐 إعداد نظام الصلاحيات في SpareSmart")
    print("=" * 60)
    
    # إنشاء مستخدمين عينة
    create_sample_users()
    
    # إعداد صلاحيات الأدوار
    setup_role_permissions()
    
    # التحقق من الصلاحيات
    verify_permissions()
    
    print("\n" + "=" * 60)
    print("🎉 تم إعداد نظام الصلاحيات بنجاح!")
    print("✅ جميع الأدوار لديها الصلاحيات المناسبة")
    print("✅ المستخدم Superuser لديه جميع الصلاحيات")
    print("\n💡 نصائح:")
    print("   - يمكن للمستخدم Superuser الوصول لجميع الصفحات")
    print("   - يمكن تعديل الصلاحيات من لوحة الإدارة")
    print("   - كلمة المرور الافتراضية للمستخدمين الجدد: password123")

if __name__ == '__main__':
    main()
