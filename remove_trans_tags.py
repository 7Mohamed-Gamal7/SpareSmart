#!/usr/bin/env python3
"""
إزالة جميع علامات {% trans %} وتحديث النصوص مباشرة بالعربية
"""
import os
import re
import glob

def clean_trans_tags(file_path):
    """إزالة علامات {% trans %} من ملف القالب"""
    
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # قاموس الترجمات الشامل
        translations = {
            # الأساسيات
            "Welcome back": "مرحباً بعودتك",
            "Here's what's happening in your spare parts business today.": "إليك ما يحدث في أعمال قطع الغيار اليوم.",
            "Dashboard": "لوحة التحكم",
            "Inventory": "المخزون",
            "Products": "المنتجات",
            "Sales": "المبيعات",
            "Purchases": "المشتريات",
            "Expenses": "المصروفات",
            "Reports": "التقارير",
            "Settings": "الإعدادات",
            
            # الإحصائيات
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
            
            # التنقل
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
            "Submit": "إرسال",
            "Update": "تحديث",
            "Create": "إنشاء",
            "Remove": "إزالة",
            
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
            "Quantity": "الكمية",
            "Code": "الكود",
            "SKU": "رقم المنتج",
            
            # الحالات
            "Active": "نشط",
            "Inactive": "غير نشط",
            "Available": "متوفر",
            "In Stock": "متوفر",
            "Low Stock": "مخزون منخفض",
            "Out of Stock": "نفد المخزون",
            "Pending": "في الانتظار",
            "Approved": "موافق عليه",
            "Rejected": "مرفوض",
            
            # الرسائل
            "Loading...": "جاري التحميل...",
            "No data available": "لا توجد بيانات",
            "No results found": "لم يتم العثور على نتائج",
            "Success": "نجح",
            "Error": "خطأ",
            "Warning": "تحذير",
            "Info": "معلومات",
            "Confirmation": "تأكيد",
            
            # التواريخ
            "Today": "اليوم",
            "Yesterday": "أمس",
            "This Week": "هذا الأسبوع",
            "This Month": "هذا الشهر",
            "Last 7 Days": "آخر 7 أيام",
            "Last 30 Days": "آخر 30 يوم",
            
            # المخزون
            "Product List": "قائمة المنتجات",
            "Add New Product": "إضافة منتج جديد",
            "Edit Product": "تعديل المنتج",
            "Product Details": "تفاصيل المنتج",
            "Categories": "الفئات",
            "Brands": "العلامات التجارية",
            "Suppliers": "الموردون",
            
            # المبيعات
            "Sale List": "قائمة المبيعات",
            "New Sale": "بيع جديد",
            "Sale Details": "تفاصيل البيع",
            "Customer": "العميل",
            "Invoice": "الفاتورة",
            
            # المشتريات
            "Purchase List": "قائمة المشتريات",
            "New Purchase": "شراء جديد",
            "Purchase Details": "تفاصيل الشراء",
            "Supplier": "المورد",
            
            # المصروفات
            "Expense List": "قائمة المصروفات",
            "New Expense": "مصروف جديد",
            "Expense Details": "تفاصيل المصروف",
            "Expense Category": "فئة المصروف",
            
            # التقارير
            "Sales Report": "تقرير المبيعات",
            "Inventory Report": "تقرير المخزون",
            "Financial Report": "التقرير المالي",
            "Monthly Report": "التقرير الشهري"
        }
        
        # إزالة علامات {% trans %} واستبدالها بالترجمة العربية
        for english, arabic in translations.items():
            # نمط للعثور على {% trans "text" %}
            pattern1 = f'{{% trans "{english}" %}}'
            content = content.replace(pattern1, arabic)
            
            # نمط للعثور على {% trans 'text' %}
            pattern2 = f"{{% trans '{english}' %}}"
            content = content.replace(pattern2, arabic)
        
        # إزالة أي علامات {% trans %} متبقية بنمط عام
        # هذا سيزيل العلامات ويترك النص الإنجليزي كما هو
        trans_pattern = r'{%\s*trans\s*["\']([^"\']*)["\']?\s*%}'
        content = re.sub(trans_pattern, r'\1', content)
        
        # إزالة {% load i18n %} إذا كان موجود
        content = re.sub(r'{%\s*load\s+i18n\s*%}', '', content)
        
        # كتابة الملف المحدث
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ خطأ في معالجة {file_path}: {e}")
        return False

def main():
    print("🧹 إزالة علامات {% trans %} وتحديث النصوص...")
    
    # البحث عن جميع ملفات HTML في مجلد templates
    template_files = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
    
    updated_count = 0
    
    for template_file in template_files:
        if clean_trans_tags(template_file):
            print(f"✅ تم تحديث: {template_file}")
            updated_count += 1
        else:
            print(f"⚪ لا توجد تغييرات: {template_file}")
    
    print(f"\n🎉 تم تحديث {updated_count} ملف من أصل {len(template_files)} ملف")
    print("✅ تم إزالة جميع علامات الترجمة وتحديث النصوص للعربية!")

if __name__ == '__main__':
    main()
