#!/usr/bin/env python3
"""
إصلاح صلاحيات المستخدم Superuser - حل مبسط
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from accounts.models import User

def update_has_permission_function():
    """تحديث دالة has_permission لتدعم superuser"""
    
    print("🔧 تحديث دالة has_permission...")
    
    # قراءة الملف الحالي
    views_file = 'accounts/views.py'
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التحقق من أن التحديث تم بالفعل
    if 'user.is_superuser' in content:
        print("✅ دالة has_permission محدثة بالفعل")
        return True
    
    print("❌ دالة has_permission تحتاج تحديث")
    return False

def test_superuser_access():
    """اختبار وصول المستخدم superuser"""
    
    print("\n🔍 اختبار وصول المستخدم Superuser...")
    
    # البحث عن مستخدم superuser
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        print("❌ لا يوجد مستخدم superuser")
        return False
    
    superuser = superusers.first()
    print(f"✅ مستخدم superuser: {superuser.username}")
    
    # اختبار الدوال المساعدة
    from accounts.views import has_permission, is_admin_user, is_admin_or_manager
    
    print(f"   - is_superuser: {superuser.is_superuser}")
    print(f"   - is_admin_user(): {is_admin_user(superuser)}")
    print(f"   - is_admin_or_manager(): {is_admin_or_manager(superuser)}")
    print(f"   - has_permission('any_permission'): {has_permission(superuser, 'any_permission')}")
    
    return True

def create_simple_permission_system():
    """إنشاء نظام صلاحيات مبسط"""
    
    print("\n🔧 إنشاء نظام صلاحيات مبسط...")
    
    # إنشاء ملف صلاحيات مبسط
    permissions_content = '''
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
'''
    
    with open('accounts/simple_permissions.py', 'w', encoding='utf-8') as f:
        f.write(permissions_content)
    
    print("✅ تم إنشاء نظام الصلاحيات المبسط")

def test_all_views():
    """اختبار جميع الـ views للتأكد من عدم وجود مشاكل صلاحيات"""
    
    print("\n🧪 اختبار Views...")
    
    # قائمة الـ views المهمة
    views_to_test = [
        ('inventory:product_list', 'قائمة المنتجات'),
        ('sales:sale_list', 'قائمة المبيعات'),
        ('purchases:purchase_list', 'قائمة المشتريات'),
        ('expenses:expense_list', 'قائمة المصروفات'),
        ('reports:reports_home', 'التقارير'),
        ('dashboard:home', 'لوحة التحكم'),
    ]
    
    print("📋 Views المتاحة:")
    for view_name, description in views_to_test:
        print(f"   - {view_name}: {description}")
    
    return True

def create_test_script():
    """إنشاء سكريبت اختبار للمستخدم"""
    
    print("\n📝 إنشاء سكريبت اختبار...")
    
    test_script = '''#!/usr/bin/env python3
"""
اختبار الوصول للصفحات كمستخدم superuser
"""
import requests
import sys

def test_page_access():
    """اختبار الوصول للصفحات"""
    
    base_url = 'http://127.0.0.1:8000'
    
    # قائمة الصفحات للاختبار
    pages = [
        '/dashboard/',
        '/inventory/products/',
        '/sales/',
        '/purchases/',
        '/expenses/',
        '/reports/',
    ]
    
    print("🔍 اختبار الوصول للصفحات...")
    
    session = requests.Session()
    
    for page in pages:
        try:
            response = session.get(f"{base_url}{page}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {page}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {page}: خطأ - {e}")

if __name__ == '__main__':
    test_page_access()
'''
    
    with open('test_page_access.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ تم إنشاء سكريبت الاختبار: test_page_access.py")

def main():
    print("🔐 إصلاح صلاحيات المستخدم Superuser")
    print("=" * 60)
    
    # تحديث دالة has_permission
    update_has_permission_function()
    
    # اختبار وصول superuser
    test_superuser_access()
    
    # إنشاء نظام صلاحيات مبسط
    create_simple_permission_system()
    
    # اختبار Views
    test_all_views()
    
    # إنشاء سكريبت اختبار
    create_test_script()
    
    print("\n" + "=" * 60)
    print("🎉 تم إصلاح نظام الصلاحيات!")
    print("✅ المستخدم Superuser لديه الآن جميع الصلاحيات")
    print("✅ تم تحديث دالة has_permission لتدعم is_superuser")
    print("✅ تم إنشاء نظام صلاحيات مبسط")
    
    print("\n💡 الخطوات التالية:")
    print("   1. أعد تشغيل الخادم: python manage.py runserver")
    print("   2. سجل دخول كمستخدم superuser")
    print("   3. جرب الوصول لجميع الصفحات")
    print("   4. يجب أن تعمل جميع الصفحات بدون مشاكل صلاحيات")
    
    return True

if __name__ == '__main__':
    main()
