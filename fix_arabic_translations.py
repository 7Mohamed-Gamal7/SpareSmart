#!/usr/bin/env python3
"""
إصلاح الترجمات العربية - إنشاء ملف .mo يعمل فعلياً
"""
import os
import struct

def create_working_mo_file():
    """إنشاء ملف .mo يحتوي على ترجمات فعلية"""
    
    # الترجمات الأساسية التي تظهر في الواجهة
    translations = {
        # الترجمات المرئية في الصورة
        "Welcome back": "مرحباً بعودتك",
        "Here's what's happening in your spare parts business today.": "إليك ما يحدث في أعمال قطع الغيار اليوم.",
        "Monthly Revenue": "الإيرادات الشهرية",
        "sales this month": "مبيعات هذا الشهر", 
        "Inventory Value": "قيمة المخزون",
        "products": "منتجات",
        "Monthly Revenue": "الإيرادات الشهرية",
        "sales this month": "مبيعات هذا الشهر",
        "Today's Sales": "مبيعات اليوم",
        "transactions": "معاملات",
        "Quick Actions": "الإجراءات السريعة",
        "New Sale": "بيع جديد",
        "New Purchase": "شراء جديد", 
        "Add Product": "إضافة منتج",
        "Record Expense": "تسجيل مصروف",
        "View Reports": "عرض التقارير",
        "Sales Trend (Last 7 Days)": "اتجاه المبيعات (آخر 7 أيام)",
        
        # القائمة الجانبية
        "Dashboard": "لوحة التحكم",
        "Inventory": "المخزون", 
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        
        # عناصر أساسية
        "SpareSmart": "سبير سمارت",
        "Products": "المنتجات",
        "Categories": "الفئات",
        "Brands": "العلامات التجارية",
        "Suppliers": "الموردون",
        "Customers": "العملاء",
        "Settings": "الإعدادات",
        "Profile": "الملف الشخصي",
        "Logout": "تسجيل الخروج",
        
        # أرقام وقيم
        "50": "50",
        "$0": "0 ج.م",
        "$50": "50 ج.م",
        
        # إجراءات
        "Add": "إضافة",
        "Edit": "تعديل", 
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "View": "عرض",
        "Search": "بحث",
        "Filter": "تصفية",
        
        # حالات
        "Active": "نشط",
        "Inactive": "غير نشط",
        "Available": "متوفر",
        "Out of Stock": "نفد المخزون",
        "Low Stock": "مخزون منخفض",
        
        # تواريخ
        "Today": "اليوم",
        "Yesterday": "أمس", 
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "Last 7 Days": "آخر 7 أيام",
        
        # رسائل
        "Loading...": "جاري التحميل...",
        "No data available": "لا توجد بيانات",
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير"
    }
    
    # إنشاء مجلد الترجمة
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    
    # إعداد البيانات للملف الثنائي
    keys = [b'']  # المفتاح الفارغ مطلوب
    values = [b'Content-Type: text/plain; charset=UTF-8\nLanguage: ar\n']  # الرأس مطلوب
    
    # إضافة الترجمات
    for english, arabic in translations.items():
        keys.append(english.encode('utf-8'))
        values.append(arabic.encode('utf-8'))
    
    # حساب المواضع
    keyoffsets = []
    valueoffsets = []
    
    # بداية البيانات بعد الجداول
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        keyoffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        valueoffsets.append((offset, len(value)))
        offset += len(value)
    
    # كتابة ملف .mo
    mo_path = 'locale/ar/LC_MESSAGES/django.mo'
    with open(mo_path, 'wb') as f:
        # Magic number (little endian)
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of strings
        f.write(struct.pack('<I', len(keys)))
        # Offset of key table
        f.write(struct.pack('<I', 7 * 4))
        # Offset of value table
        f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))
        # Hash table size (0 = no hash table)
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 0))
        
        # Key table
        for offset, length in keyoffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Value table
        for offset, length in valueoffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Keys
        for key in keys:
            f.write(key)
        
        # Values
        for value in values:
            f.write(value)
    
    print(f"✅ تم إنشاء {mo_path} مع {len(translations)} ترجمة فعلية")
    return True

def create_comprehensive_po_file():
    """إنشاء ملف .po شامل"""
    
    po_content = '''# Arabic translation for SpareSmart
# Copyright (C) 2024 SpareSmart Team
msgid ""
msgstr ""
"Project-Id-Version: SpareSmart 1.0\\n"
"Language: ar\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;\\n"

msgid "Welcome back"
msgstr "مرحباً بعودتك"

msgid "Here's what's happening in your spare parts business today."
msgstr "إليك ما يحدث في أعمال قطع الغيار اليوم."

msgid "Dashboard"
msgstr "لوحة التحكم"

msgid "Inventory"
msgstr "المخزون"

msgid "Sales"
msgstr "المبيعات"

msgid "Purchases"
msgstr "المشتريات"

msgid "Expenses"
msgstr "المصروفات"

msgid "Reports"
msgstr "التقارير"

msgid "Monthly Revenue"
msgstr "الإيرادات الشهرية"

msgid "sales this month"
msgstr "مبيعات هذا الشهر"

msgid "Inventory Value"
msgstr "قيمة المخزون"

msgid "products"
msgstr "منتجات"

msgid "Today's Sales"
msgstr "مبيعات اليوم"

msgid "transactions"
msgstr "معاملات"

msgid "Quick Actions"
msgstr "الإجراءات السريعة"

msgid "New Sale"
msgstr "بيع جديد"

msgid "New Purchase"
msgstr "شراء جديد"

msgid "Add Product"
msgstr "إضافة منتج"

msgid "Record Expense"
msgstr "تسجيل مصروف"

msgid "View Reports"
msgstr "عرض التقارير"

msgid "Sales Trend (Last 7 Days)"
msgstr "اتجاه المبيعات (آخر 7 أيام)"

msgid "SpareSmart"
msgstr "سبير سمارت"

msgid "Products"
msgstr "المنتجات"

'''
    
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(po_content)
    
    print("✅ تم إنشاء ملف .po شامل")

def main():
    print("🔧 إصلاح الترجمات العربية...")
    
    # إنشاء ملف .po
    create_comprehensive_po_file()
    
    # إنشاء ملف .mo فعال
    if create_working_mo_file():
        print("🎉 تم إصلاح الترجمات بنجاح!")
        print("🔄 يرجى إعادة تحميل الصفحة لرؤية التغييرات")
    else:
        print("❌ فشل في إصلاح الترجمات")

if __name__ == '__main__':
    main()
