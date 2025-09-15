#!/usr/bin/env python3
"""
تحديث جميع القوالب لتكون باللغة العربية
"""
import os
import re

def update_template_file(file_path, replacements):
    """تحديث ملف قالب بالترجمات العربية"""
    
    if not os.path.exists(file_path):
        print(f"الملف غير موجود: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # تطبيق الاستبدالات
        for english, arabic in replacements.items():
            # استبدال النصوص مع {% trans %}
            pattern1 = f'{{% trans "{english}" %}}'
            content = content.replace(pattern1, arabic)
            
            # استبدال النصوص مع {% trans %} والمسافات
            pattern2 = f'{{% trans \'{english}\' %}}'
            content = content.replace(pattern2, arabic)
            
            # استبدال النصوص العادية في بعض الحالات
            if english in ['SpareSmart', 'Dashboard', 'Inventory', 'Sales', 'Purchases', 'Expenses', 'Reports']:
                content = re.sub(f'>{english}<', f'>{arabic}<', content)
        
        # كتابة الملف المحدث
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ تم تحديث: {file_path}")
            return True
        else:
            print(f"⚪ لا توجد تغييرات: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تحديث {file_path}: {e}")
        return False

def main():
    print("🔄 تحديث جميع القوالب للغة العربية...")
    
    # الترجمات الأساسية
    basic_translations = {
        # العناوين الرئيسية
        "SpareSmart": "سبير سمارت",
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار",
        "Dashboard": "لوحة التحكم",
        "Inventory": "المخزون",
        "Products": "المنتجات",
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        "Settings": "الإعدادات",
        
        # المحتوى الأساسي
        "Welcome back": "مرحباً بعودتك",
        "Here's what's happening in your spare parts business today.": "إليك ما يحدث في أعمال قطع الغيار اليوم.",
        "Today's Sales": "مبيعات اليوم",
        "Monthly Revenue": "الإيرادات الشهرية",
        "Inventory Value": "قيمة المخزون",
        "Monthly Expenses": "المصروفات الشهرية",
        "transactions": "معاملات",
        "sales this month": "مبيعات هذا الشهر",
        "products": "منتجات",
        "expenses": "مصروفات",
        
        # الإجراءات
        "Quick Actions": "الإجراءات السريعة",
        "New Sale": "بيع جديد",
        "New Purchase": "شراء جديد",
        "Add Product": "إضافة منتج",
        "Record Expense": "تسجيل مصروف",
        "View Reports": "عرض التقارير",
        "Sales Trend (Last 7 Days)": "اتجاه المبيعات (آخر 7 أيام)",
        
        # القوائم والتنقل
        "Profile": "الملف الشخصي",
        "Logout": "تسجيل الخروج",
        "Notifications": "الإشعارات",
        "View All": "عرض الكل",
        
        # المصادقة
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Remember me": "تذكرني",
        "Sign in": "دخول",
        
        # الإجراءات العامة
        "Add": "إضافة",
        "Edit": "تعديل",
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "Search": "بحث",
        "Filter": "تصفية",
        "Actions": "الإجراءات",
        "View": "عرض",
        "Details": "التفاصيل",
        "Close": "إغلاق",
        
        # البيانات
        "Name": "الاسم",
        "Price": "السعر",
        "Stock": "المخزون",
        "Category": "الفئة",
        "Brand": "العلامة التجارية",
        "Description": "الوصف",
        "Status": "الحالة",
        "Date": "التاريخ",
        "Amount": "المبلغ",
        "Total": "الإجمالي",
        
        # الحالات
        "Active": "نشط",
        "Inactive": "غير نشط",
        "Available": "متوفر",
        "In Stock": "متوفر",
        "Low Stock": "مخزون منخفض",
        "Out of Stock": "نفد المخزون",
        
        # الرسائل
        "Loading...": "جاري التحميل...",
        "No data available": "لا توجد بيانات",
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير",
        "Info": "معلومات",
        
        # التواريخ
        "Today": "اليوم",
        "Yesterday": "أمس",
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "Last 7 Days": "آخر 7 أيام"
    }
    
    # القوالب المراد تحديثها
    templates_to_update = [
        'templates/base.html',
        'templates/dashboard/home.html',
        'templates/inventory/product_list.html',
        'templates/inventory/product_form.html',
        'templates/inventory/product_detail.html',
        'templates/inventory/category_list.html',
        'templates/sales/sale_list.html',
        'templates/purchases/purchase_list.html',
        'templates/expenses/expense_list.html',
        'templates/auth/login.html'
    ]
    
    updated_count = 0
    
    for template_path in templates_to_update:
        if update_template_file(template_path, basic_translations):
            updated_count += 1
    
    print(f"\n🎉 تم تحديث {updated_count} ملف من أصل {len(templates_to_update)} ملف")
    print("✅ تم تحديث النظام ليكون باللغة العربية!")
    print("🔄 يرجى إعادة تحميل الصفحة لرؤية التغييرات")

if __name__ == '__main__':
    main()
