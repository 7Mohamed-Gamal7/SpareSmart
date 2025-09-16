#!/usr/bin/env python3
"""
إنشاء ملف .mo يدوياً بدون msgfmt
"""
import os
import struct

def create_mo_file(translations, mo_path):
    """إنشاء ملف .mo يدوياً"""
    
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # إعداد البيانات
    keys = [b'']  # المفتاح الفارغ مطلوب
    values = [b'Content-Type: text/plain; charset=UTF-8\n']  # القيمة الفارغة مطلوبة
    
    # إضافة الترجمات
    for msgid, msgstr in translations.items():
        keys.append(msgid.encode('utf-8'))
        values.append(msgstr.encode('utf-8'))
    
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
        # Magic number
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
    
    print(f"تم إنشاء {mo_path} بنجاح")

def main():
    print("إنشاء ملف .mo يدوياً...")
    
    # ترجمات أساسية
    translations = {
        "Dashboard": "لوحة التحكم",
        "SpareSmart": "سبير سمارت", 
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار",
        "Products": "المنتجات",
        "Inventory": "المخزون",
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        "Settings": "الإعدادات",
        "Welcome back": "مرحباً بعودتك",
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Remember me": "تذكرني",
        "Sign in": "دخول",
        "Logout": "تسجيل الخروج",
        "Add Product": "إضافة منتج",
        "Product Management": "إدارة المنتجات",
        "Edit": "تعديل",
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "Search": "بحث",
        "Actions": "الإجراءات",
        "Name": "name",
        "Price": "price",
        "Stock": "المخزون",
        "Category": "category",
        "Brand": "brand",
        "Description": "description",
        "Add": "إضافة",
        "View": "عرض",
        "Details": "التفاصيل",
        "Close": "إغلاق",
        "Today's Sales": "مبيعات اليوم",
        "Total Revenue": "إجمالي الإيرادات",
        "Low Stock Items": "المنتجات منخفضة المخزون",
        "Pending Orders": "الطلبات المعلقة",
        "transactions": "معاملات",
        "this month": "هذا الشهر",
        "items need attention": "منتجات تحتاج انتباه",
        "orders to process": "طلبات للمعالجة",
        "Here's what's happening in your spare parts business today.": "إليك ما يحدث في أعمال قطع الغيار اليوم.",
        "Manage Categories": "إدارة الفئات",
        "Low Stock Report": "تقرير المخزون المنخفض",
        "Stock Movements": "حركات المخزون",
        "All Categories": "جميع الفئات",
        "All Brands": "جميع العلامات التجارية",
        "Loading...": "جاري التحميل...",
        "No data found": "لا توجد بيانات",
        "Search...": "بحث...",
        "Quick Actions": "الإجراءات السريعة",
        "Sell": "بيع",
        "Adjust Stock": "تعديل المخزون",
        "Clone": "نسخ",
        "Active": "active",
        "Featured": "مميز",
        "In Stock": "متوفر",
        "Low Stock": "مخزون منخفض",
        "Out of Stock": "نفد المخزون",
        "Cost Price": "cost_price",
        "Selling Price": "selling_price",
        "Current Stock": "المخزون الحالي",
        "Minimum Stock": "min_stock_level",
        "SKU": "sku",
        "Barcode": "barcode",
        "Unit": "الوحدة",
        "Weight": "الوزن",
        "Color": "اللون",
        "Image": "الصورة",
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
        "Address": "address",
        "Phone": "phone",
        "Email": "email",
        "First Name": "الاسم الأول",
        "Last Name": "اسم العائلة",
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير",
        "Info": "معلومات",
        "Are you sure?": "هل أنت متأكد؟",
        "Yes, delete it!": "نعم، احذفه!",
        "No, cancel": "لا، إلغاء",
        "This field is required.": "هذا الحقل مطلوب.",
        "Please enter a valid value.": "يرجى إدخال قيمة صحيحة.",
        "Today": "اليوم",
        "Yesterday": "أمس",
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "This Year": "هذا العام",
        "Created": "تم الإنشاء",
        "Updated": "تم التحديث",
        "Back": "رجوع",
        "Next": "التالي",
        "Previous": "السابق",
        "Print": "طباعة",
        "Export": "تصدير",
        "Import": "استيراد",
        "Filter": "تصفية",
        "All": "الكل",
        "New": "جديد",
        "Update": "تحديث",
        "Create": "إنشاء",
        "Submit": "إرسال"
    }
    
    # إنشاء ملف .mo
    create_mo_file(translations, 'locale/ar/LC_MESSAGES/django.mo')
    
    print(f"✅ تم إنشاء ملف الترجمة العربي بنجاح!")
    print(f"عدد الترجمات: {len(translations)}")

if __name__ == '__main__':
    main()
