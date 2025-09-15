#!/usr/bin/env python3
"""
إنشاء ملف .mo عربي نهائي مع ترجمات شاملة
"""
import os
import struct

def create_arabic_mo_file(translations, mo_path):
    """إنشاء ملف .mo عربي"""
    
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # إعداد البيانات
    keys = [b'']  # المفتاح الفارغ مطلوب
    values = [b'Content-Type: text/plain; charset=UTF-8\n']  # القيمة الفارغة مطلوبة
    
    # إضافة الترجمات
    for msgid, msgstr in translations.items():
        try:
            keys.append(msgid.encode('utf-8'))
            values.append(msgstr.encode('utf-8'))
        except UnicodeEncodeError:
            print(f"تخطي الترجمة: {msgid}")
            continue
    
    # حساب الإزاحات
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
    
    print(f"تم إنشاء {mo_path} بنجاح مع {len(keys)-1} ترجمة")

def main():
    print("إنشاء ملف الترجمة العربي النهائي...")
    
    # ترجمات عربية شاملة
    arabic_translations = {
        # العناوين الرئيسية
        "Dashboard": "لوحة التحكم",
        "SpareSmart": "سبير سمارت",
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار",
        
        # التنقل الرئيسي
        "Inventory": "المخزون",
        "Products": "المنتجات",
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        "Settings": "الإعدادات",
        "Profile": "الملف الشخصي",
        "Users": "المستخدمون",
        "Logout": "تسجيل الخروج",
        
        # محتوى لوحة التحكم
        "Welcome back": "مرحباً بعودتك",
        "Here's what's happening in your spare parts business today.": "إليك ما يحدث في أعمال قطع الغيار اليوم.",
        "Today's Sales": "مبيعات اليوم",
        "transactions": "معاملات",
        "Total Revenue": "إجمالي الإيرادات",
        "this month": "هذا الشهر",
        "Low Stock Items": "المنتجات منخفضة المخزون",
        "items need attention": "منتجات تحتاج انتباه",
        "Pending Orders": "الطلبات المعلقة",
        "orders to process": "طلبات للمعالجة",
        
        # إدارة المنتجات
        "Product Management": "إدارة المنتجات",
        "Add Product": "إضافة منتج",
        "Edit Product": "تعديل المنتج",
        "Product Details": "تفاصيل المنتج",
        "Product Name": "اسم المنتج",
        "Description": "description",
        "SKU": "sku",
        "Barcode": "barcode",
        "Category": "category",
        "Brand": "brand",
        "Unit": "الوحدة",
        "Cost Price": "cost_price",
        "Selling Price": "selling_price",
        "Current Stock": "المخزون الحالي",
        "Minimum Stock": "min_stock_level",
        "Weight": "الوزن",
        "Color": "اللون",
        "Image": "الصورة",
        "Active": "active",
        "Featured": "مميز",
        
        # حالة المخزون
        "In Stock": "متوفر",
        "Low Stock": "مخزون منخفض",
        "Out of Stock": "نفد المخزون",
        
        # الإجراءات الشائعة
        "Add": "إضافة",
        "Edit": "تعديل",
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "Submit": "إرسال",
        "Update": "تحديث",
        "Create": "إنشاء",
        "Search": "بحث",
        "Filter": "تصفية",
        "Export": "تصدير",
        "Import": "استيراد",
        "Print": "طباعة",
        "Back": "رجوع",
        "Next": "التالي",
        "Previous": "السابق",
        "View": "عرض",
        "Details": "التفاصيل",
        "Close": "إغلاق",
        "Actions": "الإجراءات",
        
        # المصادقة
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Remember me": "تذكرني",
        "Sign in": "دخول",
        "Sign out": "خروج",
        "First Name": "الاسم الأول",
        "Last Name": "اسم العائلة",
        "Email": "email",
        "Phone": "phone",
        "Address": "address",
        
        # البيانات الأساسية
        "Name": "name",
        "Price": "price",
        "Stock": "المخزون",
        "Status": "status",
        "Date": "date",
        "Time": "الوقت",
        "Amount": "amount",
        "Total": "الإجمالي",
        "Customer": "customer",
        "Supplier": "supplier",
        "Quantity": "quantity",
        "Unit Price": "سعر الوحدة",
        "Subtotal": "المجموع الفرعي",
        "Discount": "discount",
        "Tax": "tax",
        "Notes": "notes",
        
        # رسائل الحالة
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير",
        "Info": "معلومات",
        "Are you sure?": "هل أنت متأكد؟",
        "Yes, delete it!": "نعم، احذفه!",
        "No, cancel": "لا، إلغاء",
        
        # التحقق من النماذج
        "This field is required.": "هذا الحقل مطلوب.",
        "Please enter a valid value.": "يرجى إدخال قيمة صحيحة.",
        
        # التاريخ والوقت
        "Today": "اليوم",
        "Yesterday": "أمس",
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "This Year": "هذا العام",
        "Created": "تم الإنشاء",
        "Updated": "تم التحديث",
        
        # واجهة إضافية
        "Loading...": "جاري التحميل...",
        "No data found": "لا توجد بيانات",
        "Search...": "بحث...",
        "All Categories": "جميع الفئات",
        "All Brands": "جميع العلامات التجارية",
        "Quick Actions": "الإجراءات السريعة",
        "Sell": "بيع",
        "Adjust Stock": "تعديل المخزون",
        "Clone": "نسخ",
        "Manage Categories": "إدارة الفئات",
        "Low Stock Report": "تقرير المخزون المنخفض",
        "Stock Movements": "حركات المخزون",
        
        # إضافات مهمة
        "Categories": "الفئات",
        "Brands": "العلامات التجارية",
        "Suppliers": "الموردون",
        "Customers": "العملاء",
        "All": "الكل",
        "New": "جديد",
        "General": "عام",
        "Piece": "قطعة",
        "Set": "طقم",
        "Pair": "زوج",
        "Box": "صندوق",
        "Meter": "متر",
        "Liter": "لتر",
        "Kilogram": "كيلوغرام"
    }
    
    # إنشاء ملف .mo
    create_arabic_mo_file(arabic_translations, 'locale/ar/LC_MESSAGES/django.mo')
    
    print("✅ تم إنشاء النظام العربي الكامل بنجاح!")
    print(f"عدد الترجمات: {len(arabic_translations)}")

if __name__ == '__main__':
    main()
