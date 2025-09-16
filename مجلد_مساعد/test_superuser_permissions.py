#!/usr/bin/env python3
"""
اختبار صلاحيات المستخدم Superuser
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from accounts.models import User
from accounts.views import has_permission, is_admin_user, is_admin_or_manager

def test_superuser_permissions():
    """اختبار صلاحيات المستخدم Superuser"""
    
    print("🔍 اختبار صلاحيات المستخدم Superuser...")
    print("=" * 60)
    
    # البحث عن مستخدم superuser
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        print("❌ لا يوجد مستخدم superuser في النظام")
        print("💡 يمكنك إنشاء مستخدم superuser باستخدام:")
        print("   python manage.py createsuperuser")
        return False
    
    superuser = superusers.first()
    print(f"✅ تم العثور على مستخدم superuser: {superuser.username}")
    print(f"   - الاسم: {superuser.first_name} {superuser.last_name}")
    print(f"   - البريد الإلكتروني: {superuser.email}")
    print(f"   - الدور: {superuser.get_role_display()}")
    print(f"   - is_superuser: {superuser.is_superuser}")
    print(f"   - is_staff: {superuser.is_staff}")
    print()
    
    # اختبار الدوال المساعدة
    print("🧪 اختبار الدوال المساعدة:")
    print(f"   - is_admin_user(): {is_admin_user(superuser)}")
    print(f"   - is_admin_or_manager(): {is_admin_or_manager(superuser)}")
    print()
    
    # اختبار الصلاحيات المختلفة
    permissions_to_test = [
        'view_products',
        'add_products', 
        'change_products',
        'delete_products',
        'view_sales',
        'add_sales',
        'change_sales',
        'delete_sales',
        'view_purchases',
        'add_purchases',
        'change_purchases',
        'delete_purchases',
        'view_expenses',
        'add_expenses',
        'change_expenses',
        'delete_expenses',
        'process_payments',
        'view_reports',
        'generate_reports',
        'manage_users',
        'manage_settings'
    ]
    
    print("🔐 اختبار الصلاحيات:")
    all_passed = True
    
    for permission in permissions_to_test:
        has_perm = has_permission(superuser, permission)
        status = "✅" if has_perm else "❌"
        print(f"   {status} {permission}: {has_perm}")
        if not has_perm:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 جميع اختبارات الصلاحيات نجحت!")
        print("✅ المستخدم Superuser لديه جميع الصلاحيات")
    else:
        print("⚠️  بعض الصلاحيات لا تعمل بشكل صحيح")
    
    return all_passed

def test_regular_users():
    """اختبار المستخدمين العاديين"""
    
    print("\n" + "=" * 60)
    print("🔍 اختبار المستخدمين العاديين...")
    
    # اختبار مستخدم admin
    admin_users = User.objects.filter(role='admin', is_superuser=False)
    if admin_users.exists():
        admin_user = admin_users.first()
        print(f"\n👤 مستخدم Admin: {admin_user.username}")
        print(f"   - is_admin_user(): {is_admin_user(admin_user)}")
        print(f"   - is_admin_or_manager(): {is_admin_or_manager(admin_user)}")
        print(f"   - has_permission('view_products'): {has_permission(admin_user, 'view_products')}")
    
    # اختبار مستخدم manager
    manager_users = User.objects.filter(role='manager')
    if manager_users.exists():
        manager_user = manager_users.first()
        print(f"\n👤 مستخدم Manager: {manager_user.username}")
        print(f"   - is_admin_user(): {is_admin_user(manager_user)}")
        print(f"   - is_admin_or_manager(): {is_admin_or_manager(manager_user)}")
        print(f"   - has_permission('view_products'): {has_permission(manager_user, 'view_products')}")
    
    # اختبار مستخدم viewer
    viewer_users = User.objects.filter(role='viewer')
    if viewer_users.exists():
        viewer_user = viewer_users.first()
        print(f"\n👤 مستخدم Viewer: {viewer_user.username}")
        print(f"   - is_admin_user(): {is_admin_user(viewer_user)}")
        print(f"   - is_admin_or_manager(): {is_admin_or_manager(viewer_user)}")
        print(f"   - has_permission('view_products'): {has_permission(viewer_user, 'view_products')}")

def create_test_permissions():
    """إنشاء صلاحيات اختبارية إذا لم تكن موجودة"""
    
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    from accounts.models import RolePermission
    
    print("\n" + "=" * 60)
    print("🔧 إنشاء الصلاحيات الاختبارية...")
    
    # الحصول على content type للمستخدم
    user_ct = ContentType.objects.get_for_model(User)
    
    # قائمة الصلاحيات المطلوبة
    permissions_data = [
        ('view_products', 'Can view products'),
        ('add_products', 'Can add products'),
        ('change_products', 'Can change products'),
        ('delete_products', 'Can delete products'),
        ('view_sales', 'Can view sales'),
        ('add_sales', 'Can add sales'),
        ('change_sales', 'Can change sales'),
        ('delete_sales', 'Can delete sales'),
        ('view_purchases', 'Can view purchases'),
        ('add_purchases', 'Can add purchases'),
        ('change_purchases', 'Can change purchases'),
        ('delete_purchases', 'Can delete purchases'),
        ('view_expenses', 'Can view expenses'),
        ('add_expenses', 'Can add expenses'),
        ('change_expenses', 'Can change expenses'),
        ('delete_expenses', 'Can delete expenses'),
        ('process_payments', 'Can process payments'),
        ('view_reports', 'Can view reports'),
        ('generate_reports', 'Can generate reports'),
        ('manage_users', 'Can manage users'),
        ('manage_settings', 'Can manage settings'),
    ]
    
    created_count = 0
    
    for codename, name in permissions_data:
        permission, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=user_ct,
            defaults={'name': name}
        )
        if created:
            created_count += 1
            print(f"   ✅ تم إنشاء صلاحية: {name}")
    
    if created_count > 0:
        print(f"\n🎉 تم إنشاء {created_count} صلاحية جديدة")
    else:
        print("\n✅ جميع الصلاحيات موجودة بالفعل")

def main():
    print("🔐 اختبار نظام الصلاحيات في SpareSmart")
    print("=" * 60)
    
    # إنشاء الصلاحيات الاختبارية
    create_test_permissions()
    
    # اختبار صلاحيات superuser
    superuser_ok = test_superuser_permissions()
    
    # اختبار المستخدمين العاديين
    test_regular_users()
    
    print("\n" + "=" * 60)
    
    if superuser_ok:
        print("🎉 نظام الصلاحيات يعمل بشكل صحيح!")
        print("✅ المستخدم Superuser لديه جميع الصلاحيات")
        print("✅ يمكن للمستخدم Superuser الوصول لجميع الصفحات")
    else:
        print("⚠️  توجد مشاكل في نظام الصلاحيات")
        print("💡 تأكد من وجود الصلاحيات في قاعدة البيانات")
    
    return superuser_ok

if __name__ == '__main__':
    main()
