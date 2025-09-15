#!/usr/bin/env python3
"""
Create comprehensive Arabic translation files for SpareSmart system
"""
import os
import struct

def create_comprehensive_arabic_po():
    """Create comprehensive Arabic .po file with all translations"""
    
    po_content = '''# Arabic translation for SpareSmart - Comprehensive
# Copyright (C) 2024 SpareSmart Team
# This file is distributed under the same license as the SpareSmart package.
#
msgid ""
msgstr ""
"Project-Id-Version: SpareSmart 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-01-15 14:00+0200\\n"
"PO-Revision-Date: 2025-01-15 14:00+0200\\n"
"Last-Translator: SpareSmart Team\\n"
"Language: ar\\n"
"Language-Team: Arabic\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;\\n"

# Application Name and Title
msgid "SpareSmart"
msgstr "سبير سمارت"

msgid "SpareSmart - Spare Parts Management"
msgstr "سبير سمارت - إدارة قطع الغيار"

# Main Navigation
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

msgid "Settings"
msgstr "الإعدادات"

msgid "Profile"
msgstr "الملف الشخصي"

msgid "Users"
msgstr "المستخدمون"

msgid "Logout"
msgstr "تسجيل الخروج"

# Dashboard Content
msgid "Welcome back"
msgstr "مرحباً بعودتك"

msgid "Here's what's happening in your spare parts business today."
msgstr "إليك ما يحدث في أعمال قطع الغيار اليوم."

msgid "Today's Sales"
msgstr "مبيعات اليوم"

msgid "transactions"
msgstr "معاملات"

msgid "Total Revenue"
msgstr "إجمالي الإيرادات"

msgid "this month"
msgstr "هذا الشهر"

msgid "Low Stock Items"
msgstr "المنتجات منخفضة المخزون"

msgid "items need attention"
msgstr "منتجات تحتاج انتباه"

msgid "Pending Orders"
msgstr "الطلبات المعلقة"

msgid "orders to process"
msgstr "طلبات للمعالجة"

msgid "Sales Trend"
msgstr "اتجاه المبيعات"

msgid "Last 7 Days"
msgstr "آخر 7 أيام"

msgid "Sales Amount"
msgstr "مبلغ المبيعات"

msgid "Top Selling Products"
msgstr "المنتجات الأكثر مبيعاً"

msgid "Recent Activities"
msgstr "الأنشطة الحديثة"

msgid "View All"
msgstr "عرض الكل"

# Inventory Module
msgid "Products"
msgstr "المنتجات"

msgid "Categories"
msgstr "الفئات"

msgid "Brands"
msgstr "العلامات التجارية"

msgid "Suppliers"
msgstr "الموردون"

msgid "Customers"
msgstr "العملاء"

msgid "Stock Movements"
msgstr "حركات المخزون"

msgid "Alerts"
msgstr "التنبيهات"

msgid "Add Product"
msgstr "إضافة منتج"

msgid "Edit Product"
msgstr "تعديل المنتج"

msgid "Product Details"
msgstr "تفاصيل المنتج"

msgid "Product Name"
msgstr "اسم المنتج"

msgid "Description"
msgstr "الوصف"

msgid "SKU"
msgstr "رمز المنتج"

msgid "Barcode"
msgstr "الباركود"

msgid "Category"
msgstr "الفئة"

msgid "Brand"
msgstr "العلامة التجارية"

msgid "Unit"
msgstr "الوحدة"

msgid "Cost Price"
msgstr "سعر التكلفة"

msgid "Selling Price"
msgstr "سعر البيع"

msgid "Wholesale Price"
msgstr "سعر الجملة"

msgid "Current Stock"
msgstr "المخزون الحالي"

msgid "Minimum Stock"
msgstr "الحد الأدنى للمخزون"

msgid "Maximum Stock"
msgstr "الحد الأقصى للمخزون"

msgid "Reorder Level"
msgstr "مستوى إعادة الطلب"

msgid "Weight"
msgstr "الوزن"

msgid "Dimensions"
msgstr "الأبعاد"

msgid "Color"
msgstr "اللون"

msgid "Material"
msgstr "المادة"

msgid "Image"
msgstr "الصورة"

msgid "Compatible Vehicles"
msgstr "المركبات المتوافقة"

msgid "Part Number"
msgstr "رقم القطعة"

msgid "OEM Number"
msgstr "رقم الشركة المصنعة"

msgid "Active"
msgstr "نشط"

msgid "Featured"
msgstr "مميز"

# Vehicle Types
msgid "Motorcycle"
msgstr "دراجة نارية"

msgid "Car"
msgstr "سيارة"

msgid "Tuk-Tuk"
msgstr "توك توك"

msgid "General"
msgstr "عام"

# Units
msgid "Piece"
msgstr "قطعة"

msgid "Set"
msgstr "طقم"

msgid "Pair"
msgstr "زوج"

msgid "Meter"
msgstr "متر"

msgid "Liter"
msgstr "لتر"

msgid "Kilogram"
msgstr "كيلوغرام"

msgid "Box"
msgstr "صندوق"

# Stock Status
msgid "In Stock"
msgstr "متوفر"

msgid "Low Stock"
msgstr "مخزون منخفض"

msgid "Out of Stock"
msgstr "نفد المخزون"

msgid "Minimum"
msgstr "الحد الأدنى"

# Sales Module
msgid "New Sale"
msgstr "بيع جديد"

msgid "Sale Details"
msgstr "تفاصيل البيع"

msgid "Customer"
msgstr "العميل"

msgid "Sale Date"
msgstr "تاريخ البيع"

msgid "Due Date"
msgstr "تاريخ الاستحقاق"

msgid "Sale Type"
msgstr "نوع البيع"

msgid "Cash"
msgstr "نقدي"

msgid "Credit"
msgstr "آجل"

msgid "Installment"
msgstr "تقسيط"

msgid "Discount Amount"
msgstr "مبلغ الخصم"

msgid "Total Amount"
msgstr "المبلغ الإجمالي"

msgid "Paid Amount"
msgstr "المبلغ المدفوع"

msgid "Remaining Amount"
msgstr "المبلغ المتبقي"

msgid "Notes"
msgstr "ملاحظات"

msgid "Internal Notes"
msgstr "ملاحظات داخلية"

msgid "Invoice"
msgstr "فاتورة"

msgid "Print Invoice"
msgstr "طباعة الفاتورة"

msgid "Payment"
msgstr "الدفع"

msgid "Add Payment"
msgstr "إضافة دفعة"

msgid "Payment Method"
msgstr "طريقة الدفع"

msgid "Payment Date"
msgstr "تاريخ الدفع"

msgid "Amount"
msgstr "المبلغ"

# Customer Types
msgid "Individual"
msgstr "فرد"

msgid "Company"
msgstr "شركة"

msgid "Retailer"
msgstr "تاجر تجزئة"

msgid "Wholesaler"
msgstr "تاجر جملة"

# Common Actions
msgid "Add"
msgstr "إضافة"

msgid "Edit"
msgstr "تعديل"

msgid "Delete"
msgstr "حذف"

msgid "Save"
msgstr "حفظ"

msgid "Cancel"
msgstr "إلغاء"

msgid "Submit"
msgstr "إرسال"

msgid "Update"
msgstr "تحديث"

msgid "Create"
msgstr "إنشاء"

msgid "Search"
msgstr "بحث"

msgid "Filter"
msgstr "تصفية"

msgid "Export"
msgstr "تصدير"

msgid "Import"
msgstr "استيراد"

msgid "Print"
msgstr "طباعة"

msgid "Download"
msgstr "تحميل"

msgid "Upload"
msgstr "رفع"

msgid "Back"
msgstr "رجوع"

msgid "Next"
msgstr "التالي"

msgid "Previous"
msgstr "السابق"

msgid "First"
msgstr "الأول"

msgid "Last"
msgstr "الأخير"

msgid "Show _MENU_ entries"
msgstr "عرض _MENU_ إدخال"

msgid "Showing _START_ to _END_ of _TOTAL_ entries"
msgstr "عرض _START_ إلى _END_ من _TOTAL_ إدخال"

msgid "No data found"
msgstr "لا توجد بيانات"

msgid "Loading..."
msgstr "جاري التحميل..."

# Status Messages
msgid "Success"
msgstr "نجح"

msgid "Error"
msgstr "خطأ"

msgid "Warning"
msgstr "تحذير"

msgid "Info"
msgstr "معلومات"

msgid "Confirmation"
msgstr "تأكيد"

msgid "Are you sure?"
msgstr "هل أنت متأكد؟"

msgid "This action cannot be undone."
msgstr "لا يمكن التراجع عن هذا الإجراء."

msgid "Yes, delete it!"
msgstr "نعم، احذفه!"

msgid "No, cancel"
msgstr "لا، إلغاء"

# Form Validation
msgid "This field is required."
msgstr "هذا الحقل مطلوب."

msgid "Please enter a valid value."
msgstr "يرجى إدخال قيمة صحيحة."

msgid "Please enter a valid email address."
msgstr "يرجى إدخال عنوان بريد إلكتروني صحيح."

msgid "Please enter a valid phone number."
msgstr "يرجى إدخال رقم هاتف صحيح."

msgid "Password is too short."
msgstr "كلمة المرور قصيرة جداً."

msgid "Passwords do not match."
msgstr "كلمات المرور غير متطابقة."

# Authentication
msgid "Login"
msgstr "تسجيل الدخول"

msgid "Username"
msgstr "اسم المستخدم"

msgid "Password"
msgstr "كلمة المرور"

msgid "Remember me"
msgstr "تذكرني"

msgid "Forgot password?"
msgstr "نسيت كلمة المرور؟"

msgid "Sign in"
msgstr "دخول"

msgid "Sign out"
msgstr "خروج"

msgid "Register"
msgstr "تسجيل"

msgid "First Name"
msgstr "الاسم الأول"

msgid "Last Name"
msgstr "اسم العائلة"

msgid "Email"
msgstr "البريد الإلكتروني"

msgid "Phone"
msgstr "الهاتف"

msgid "Address"
msgstr "العنوان"

msgid "Role"
msgstr "الدور"

msgid "Admin"
msgstr "مدير"

msgid "Manager"
msgstr "مدير"

msgid "Employee"
msgstr "موظف"

msgid "Cashier"
msgstr "أمين صندوق"

# Date and Time
msgid "Today"
msgstr "اليوم"

msgid "Yesterday"
msgstr "أمس"

msgid "This Week"
msgstr "هذا الأسبوع"

msgid "This Month"
msgstr "هذا الشهر"

msgid "This Year"
msgstr "هذا العام"

msgid "Date"
msgstr "التاريخ"

msgid "Time"
msgstr "الوقت"

msgid "Created"
msgstr "تم الإنشاء"

msgid "Updated"
msgstr "تم التحديث"

msgid "Created at"
msgstr "تم الإنشاء في"

msgid "Updated at"
msgstr "تم التحديث في"
'''
    
    return po_content

def create_minimal_mo_file(translations, mo_path):
    """Create a minimal .mo file from translations dictionary"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    if not translations:
        # Create empty .mo file
        with open(mo_path, 'wb') as f:
            f.write(struct.pack('<I', 0x950412de))  # Magic number
            f.write(struct.pack('<I', 0))           # Version
            f.write(struct.pack('<I', 0))           # Number of strings
            f.write(struct.pack('<I', 28))          # Offset of key table
            f.write(struct.pack('<I', 28))          # Offset of value table
            f.write(struct.pack('<I', 0))           # Hash table size
            f.write(struct.pack('<I', 0))           # Offset of hash table
        return
    
    # Convert to bytes
    keys = []
    values = []
    
    for msgid, msgstr in translations.items():
        try:
            key_bytes = msgid.encode('utf-8')
            value_bytes = msgstr.encode('utf-8')
            keys.append(key_bytes)
            values.append(value_bytes)
        except UnicodeEncodeError:
            print(f"Skipping invalid translation: {msgid}")
            continue
    
    if not keys:
        print("No valid translations found")
        return
    
    # Calculate offsets
    koffsets = []
    voffsets = []
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        koffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        voffsets.append((offset, len(value)))
        offset += len(value)
    
    # Write .mo file
    with open(mo_path, 'wb') as f:
        f.write(struct.pack('<I', 0x950412de))  # Magic number
        f.write(struct.pack('<I', 0))           # Version
        f.write(struct.pack('<I', len(keys)))   # Number of strings
        f.write(struct.pack('<I', 7 * 4))       # Offset of key table
        f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))  # Offset of value table
        f.write(struct.pack('<I', 0))           # Hash table size
        f.write(struct.pack('<I', 0))           # Offset of hash table
        
        # Write key table
        for offset, length in koffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write value table
        for offset, length in voffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write keys and values
        for key in keys:
            f.write(key)
        for value in values:
            f.write(value)

def main():
    print("Creating comprehensive Arabic translation files...")
    
    # Create directories
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    
    # Create Arabic .po file
    ar_po_content = create_comprehensive_arabic_po()
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(ar_po_content)
    print("Created comprehensive Arabic .po file")
    
    # Create basic English .po file
    en_po_content = ar_po_content.replace('msgstr "', 'msgstr "').replace('"ar"', '"en"').replace('Arabic', 'English')
    # Replace Arabic translations with English ones (basic mapping)
    en_translations = {
        "سبير سمارت": "SpareSmart",
        "سبير سمارت - إدارة قطع الغيار": "SpareSmart - Spare Parts Management",
        "لوحة التحكم": "Dashboard",
        "المخزون": "Inventory",
        "المبيعات": "Sales",
        "المشتريات": "Purchases",
        "المصروفات": "Expenses",
        "التقارير": "Reports",
        "الإعدادات": "Settings",
        "الملف الشخصي": "Profile",
        "المستخدمون": "Users",
        "تسجيل الخروج": "Logout"
    }
    
    for ar_text, en_text in en_translations.items():
        en_po_content = en_po_content.replace(f'msgstr "{ar_text}"', f'msgstr "{en_text}"')
    
    with open('locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(en_po_content)
    print("Created English .po file")
    
    # Create comprehensive working .mo files with all translations
    comprehensive_translations = {
        # Application Name and Title
        "SpareSmart": "سبير سمارت",
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار",

        # Main Navigation
        "Dashboard": "لوحة التحكم",
        "Inventory": "المخزون",
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        "Settings": "الإعدادات",
        "Profile": "الملف الشخصي",
        "Users": "المستخدمون",
        "Logout": "تسجيل الخروج",

        # Dashboard Content
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
        "Sales Trend": "اتجاه المبيعات",
        "Last 7 Days": "آخر 7 أيام",
        "Sales Amount": "مبلغ المبيعات",
        "Top Selling Products": "المنتجات الأكثر مبيعاً",
        "Recent Activities": "الأنشطة الحديثة",
        "View All": "عرض الكل",

        # Inventory Module
        "Products": "المنتجات",
        "Categories": "الفئات",
        "Brands": "العلامات التجارية",
        "Suppliers": "الموردون",
        "Customers": "العملاء",
        "Stock Movements": "حركات المخزون",
        "Alerts": "التنبيهات",
        "Add Product": "إضافة منتج",
        "Edit Product": "تعديل المنتج",
        "Product Details": "تفاصيل المنتج",
        "Product Name": "اسم المنتج",
        "Description": "الوصف",
        "SKU": "رمز المنتج",
        "Barcode": "الباركود",
        "Category": "الفئة",
        "Brand": "العلامة التجارية",
        "Unit": "الوحدة",
        "Cost Price": "سعر التكلفة",
        "Selling Price": "سعر البيع",
        "Wholesale Price": "سعر الجملة",
        "Current Stock": "المخزون الحالي",
        "Minimum Stock": "الحد الأدنى للمخزون",
        "Maximum Stock": "الحد الأقصى للمخزون",
        "Reorder Level": "مستوى إعادة الطلب",
        "Weight": "الوزن",
        "Dimensions": "الأبعاد",
        "Color": "اللون",
        "Material": "المادة",
        "Image": "الصورة",
        "Compatible Vehicles": "المركبات المتوافقة",
        "Part Number": "رقم القطعة",
        "OEM Number": "رقم الشركة المصنعة",
        "Active": "نشط",
        "Featured": "مميز",

        # Vehicle Types
        "Motorcycle": "دراجة نارية",
        "Car": "سيارة",
        "Tuk-Tuk": "توك توك",
        "General": "عام",

        # Units
        "Piece": "قطعة",
        "Set": "طقم",
        "Pair": "زوج",
        "Meter": "متر",
        "Liter": "لتر",
        "Kilogram": "كيلوغرام",
        "Box": "صندوق",

        # Stock Status
        "In Stock": "متوفر",
        "Low Stock": "مخزون منخفض",
        "Out of Stock": "نفد المخزون",
        "Minimum": "الحد الأدنى",

        # Sales Module
        "New Sale": "بيع جديد",
        "Sale Details": "تفاصيل البيع",
        "Customer": "العميل",
        "Sale Date": "تاريخ البيع",
        "Due Date": "تاريخ الاستحقاق",
        "Sale Type": "نوع البيع",
        "Cash": "نقدي",
        "Credit": "آجل",
        "Installment": "تقسيط",
        "Discount Amount": "مبلغ الخصم",
        "Total Amount": "المبلغ الإجمالي",
        "Paid Amount": "المبلغ المدفوع",
        "Remaining Amount": "المبلغ المتبقي",
        "Notes": "ملاحظات",
        "Internal Notes": "ملاحظات داخلية",
        "Invoice": "فاتورة",
        "Print Invoice": "طباعة الفاتورة",
        "Payment": "الدفع",
        "Add Payment": "إضافة دفعة",
        "Payment Method": "طريقة الدفع",
        "Payment Date": "تاريخ الدفع",
        "Amount": "المبلغ",

        # Customer Types
        "Individual": "فرد",
        "Company": "شركة",
        "Retailer": "تاجر تجزئة",
        "Wholesaler": "تاجر جملة",

        # Common Actions
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
        "Download": "تحميل",
        "Upload": "رفع",
        "Back": "رجوع",
        "Next": "التالي",
        "Previous": "السابق",
        "First": "الأول",
        "Last": "الأخير",

        # Status Messages
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير",
        "Info": "معلومات",
        "Confirmation": "تأكيد",
        "Are you sure?": "هل أنت متأكد؟",
        "This action cannot be undone.": "لا يمكن التراجع عن هذا الإجراء.",
        "Yes, delete it!": "نعم، احذفه!",
        "No, cancel": "لا، إلغاء",

        # Form Validation
        "This field is required.": "هذا الحقل مطلوب.",
        "Please enter a valid value.": "يرجى إدخال قيمة صحيحة.",
        "Please enter a valid email address.": "يرجى إدخال عنوان بريد إلكتروني صحيح.",
        "Please enter a valid phone number.": "يرجى إدخال رقم هاتف صحيح.",

        # Authentication
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Remember me": "تذكرني",
        "Forgot password?": "نسيت كلمة المرور؟",
        "Sign in": "دخول",
        "Sign out": "خروج",
        "Register": "تسجيل",
        "First Name": "الاسم الأول",
        "Last Name": "اسم العائلة",
        "Email": "البريد الإلكتروني",
        "Phone": "الهاتف",
        "Address": "العنوان",
        "Role": "الدور",
        "Admin": "مدير",
        "Manager": "مدير",
        "Employee": "موظف",
        "Cashier": "أمين صندوق",

        # Date and Time
        "Today": "اليوم",
        "Yesterday": "أمس",
        "This Week": "هذا الأسبوع",
        "This Month": "هذا الشهر",
        "This Year": "هذا العام",
        "Date": "التاريخ",
        "Time": "الوقت",
        "Created": "تم الإنشاء",
        "Updated": "تم التحديث",
        "Created at": "تم الإنشاء في",
        "Updated at": "تم التحديث في",

        # Additional translations for comprehensive coverage
        "Purchase Order": "أمر شراء",
        "New Purchase": "شراء جديد",
        "Supplier": "المورد",
        "Purchase Date": "تاريخ الشراء",
        "Quantity": "الكمية",
        "Unit Price": "سعر الوحدة",
        "Total": "الإجمالي",
        "Expense": "مصروف",
        "New Expense": "مصروف جديد",
        "Sales Report": "تقرير المبيعات",
        "Generate Report": "إنشاء تقرير",
        "Stock In": "إدخال مخزون",
        "Stock Out": "إخراج مخزون",
        "Low Stock Alert": "تنبيه مخزون منخفض",
        "User Management": "إدارة المستخدمين",
        "Add User": "إضافة مستخدم",
        "General Settings": "الإعدادات العامة",
        "Company Name": "اسم الشركة",
        "Quick Sale": "بيع سريع",
        "Revenue": "الإيرادات",
        "Profit": "الربح"
    }
    
    create_minimal_mo_file(comprehensive_translations, 'locale/ar/LC_MESSAGES/django.mo')
    print("Created comprehensive Arabic .mo file")

    # Create English .mo file
    en_comprehensive_translations = {k: k for k in comprehensive_translations.keys()}
    create_minimal_mo_file(en_comprehensive_translations, 'locale/en/LC_MESSAGES/django.mo')
    print("Created English .mo file")
    
    print("Translation files created successfully!")

if __name__ == '__main__':
    main()
