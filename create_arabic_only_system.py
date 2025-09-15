#!/usr/bin/env python3
"""
إنشاء نظام عربي بالكامل - حذف الإنجليزية وإنشاء ترجمات عربية شاملة
"""
import os
import struct
import shutil

def create_comprehensive_arabic_mo(translations, mo_path):
    """إنشاء ملف .mo عربي شامل"""
    
    # التأكد من وجود المجلد
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    if not translations:
        print(f"لا توجد ترجمات لإنشاء {mo_path}")
        return
    
    # تحويل إلى bytes
    keys = []
    values = []
    
    # إضافة الإدخال الفارغ (مطلوب لملفات .mo)
    keys.append(b'')
    values.append(b'Content-Type: text/plain; charset=UTF-8\n')
    
    for msgid, msgstr in translations.items():
        try:
            key_bytes = msgid.encode('utf-8')
            value_bytes = msgstr.encode('utf-8')
            keys.append(key_bytes)
            values.append(value_bytes)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(f"تخطي الترجمة المشكوك فيها: {msgid} -> {msgstr} ({e})")
            continue
    
    if len(keys) <= 1:
        print("لا توجد ترجمات صالحة")
        return
    
    # حساب المواضع
    koffsets = []
    voffsets = []
    
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        koffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        voffsets.append((offset, len(value)))
        offset += len(value)
    
    # كتابة ملف .mo
    try:
        with open(mo_path, 'wb') as f:
            # كتابة الرأس
            f.write(struct.pack('<I', 0x950412de))  # Magic number
            f.write(struct.pack('<I', 0))           # Version
            f.write(struct.pack('<I', len(keys)))   # Number of strings
            f.write(struct.pack('<I', 7 * 4))       # Offset of key table
            f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))  # Offset of value table
            f.write(struct.pack('<I', 0))           # Hash table size
            f.write(struct.pack('<I', 0))           # Offset of hash table
            
            # كتابة جدول المفاتيح
            for offset, length in koffsets:
                f.write(struct.pack('<II', length, offset))
            
            # كتابة جدول القيم
            for offset, length in voffsets:
                f.write(struct.pack('<II', length, offset))
            
            # كتابة المفاتيح والقيم
            for key in keys:
                f.write(key)
            for value in values:
                f.write(value)
                
        print(f"تم إنشاء {mo_path} بنجاح مع {len(keys)-1} ترجمة")
        
    except Exception as e:
        print(f"خطأ في إنشاء ملف .mo {mo_path}: {e}")

def main():
    print("إنشاء نظام عربي بالكامل...")
    
    # حذف ملفات الترجمة الإنجليزية
    if os.path.exists('locale/en'):
        shutil.rmtree('locale/en')
        print("تم حذف ملفات الترجمة الإنجليزية")
    
    # إنشاء مجلد الترجمة العربية
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    
    # ترجمات عربية شاملة لجميع أجزاء النظام
    comprehensive_arabic_translations = {
        # اسم التطبيق والعنوان
        "SpareSmart": "سبير سمارت",
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار",
        
        # التنقل الرئيسي
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
        "Sales Trend": "اتجاه المبيعات",
        "Last 7 Days": "آخر 7 أيام",
        "Sales Amount": "مبلغ المبيعات",
        "Top Selling Products": "المنتجات الأكثر مبيعاً",
        "Recent Activities": "الأنشطة الحديثة",
        "View All": "عرض الكل",
        
        # وحدة المخزون
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
        
        # أنواع المركبات
        "Motorcycle": "دراجة نارية",
        "Car": "سيارة",
        "Tuk-Tuk": "توك توك",
        "General": "عام",
        
        # الوحدات
        "Piece": "قطعة",
        "Set": "طقم",
        "Pair": "زوج",
        "Meter": "متر",
        "Liter": "لتر",
        "Kilogram": "كيلوغرام",
        "Box": "صندوق",
        
        # حالة المخزون
        "In Stock": "متوفر",
        "Low Stock": "مخزون منخفض",
        "Out of Stock": "نفد المخزون",
        "Minimum": "الحد الأدنى",
        
        # وحدة المبيعات
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
        
        # أنواع العملاء
        "Individual": "فرد",
        "Company": "شركة",
        "Retailer": "تاجر تجزئة",
        "Wholesaler": "تاجر جملة",
        
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
        "Download": "تحميل",
        "Upload": "رفع",
        "Back": "رجوع",
        "Next": "التالي",
        "Previous": "السابق",
        "First": "الأول",
        "Last": "الأخير",
        
        # رسائل الحالة
        "Success": "نجح",
        "Error": "خطأ",
        "Warning": "تحذير",
        "Info": "معلومات",
        "Confirmation": "تأكيد",
        "Are you sure?": "هل أنت متأكد؟",
        "This action cannot be undone.": "لا يمكن التراجع عن هذا الإجراء.",
        "Yes, delete it!": "نعم، احذفه!",
        "No, cancel": "لا، إلغاء",
        
        # التحقق من النماذج
        "This field is required.": "هذا الحقل مطلوب.",
        "Please enter a valid value.": "يرجى إدخال قيمة صحيحة.",
        "Please enter a valid email address.": "يرجى إدخال عنوان بريد إلكتروني صحيح.",
        "Please enter a valid phone number.": "يرجى إدخال رقم هاتف صحيح.",
        
        # المصادقة
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
        
        # التاريخ والوقت
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
        
        # عناصر واجهة إضافية
        "Product Management": "إدارة المنتجات",
        "Actions": "الإجراءات",
        "Manage Categories": "إدارة الفئات",
        "Low Stock Report": "تقرير المخزون المنخفض",
        "Loading...": "جاري التحميل...",
        "No data found": "لا توجد بيانات",
        "Show _MENU_ entries": "عرض _MENU_ إدخال",
        "Showing _START_ to _END_ of _TOTAL_ entries": "عرض _START_ إلى _END_ من _TOTAL_ إدخال",
        "Search...": "بحث...",
        "All Categories": "جميع الفئات",
        "All Brands": "جميع العلامات التجارية",
        "All Vehicle Types": "جميع أنواع المركبات",
        "All Stock Status": "جميع حالات المخزون",
        "Name": "الاسم",
        "Price": "السعر",
        "Stock": "المخزون",
        "View": "عرض",
        "Details": "التفاصيل",
        "Quick Actions": "الإجراءات السريعة",
        "Sell": "بيع",
        "Adjust Stock": "تعديل المخزون",
        "Clone": "نسخ",
        "Close": "إغلاق",
        
        # المشتريات
        "Purchase Order": "أمر شراء",
        "New Purchase": "شراء جديد",
        "Purchase Details": "تفاصيل الشراء",
        "Supplier": "المورد",
        "Purchase Date": "تاريخ الشراء",
        "Expected Date": "التاريخ المتوقع",
        "Purchase Status": "حالة الشراء",
        "Pending": "معلق",
        "Confirmed": "مؤكد",
        "Received": "مستلم",
        "Cancelled": "ملغي",
        "Purchase Items": "عناصر الشراء",
        "Quantity": "الكمية",
        "Unit Price": "سعر الوحدة",
        "Subtotal": "المجموع الفرعي",
        "Tax": "الضريبة",
        "Total": "الإجمالي",
        
        # المصروفات
        "Expense": "مصروف",
        "New Expense": "مصروف جديد",
        "Expense Details": "تفاصيل المصروف",
        "Expense Category": "فئة المصروف",
        "Expense Date": "تاريخ المصروف",
        "Expense Amount": "مبلغ المصروف",
        "Receipt": "إيصال",
        "Approved": "موافق عليه",
        "Rejected": "مرفوض",
        
        # التقارير
        "Sales Report": "تقرير المبيعات",
        "Purchase Report": "تقرير المشتريات",
        "Inventory Report": "تقرير المخزون",
        "Financial Report": "التقرير المالي",
        "Customer Report": "تقرير العملاء",
        "Supplier Report": "تقرير الموردين",
        "Generate Report": "إنشاء تقرير",
        "From Date": "من تاريخ",
        "To Date": "إلى تاريخ",
        "Report Type": "نوع التقرير",
        "Export to PDF": "تصدير إلى PDF",
        "Export to Excel": "تصدير إلى Excel",
        
        # إدارة المخزون
        "Stock In": "إدخال مخزون",
        "Stock Out": "إخراج مخزون",
        "Stock Adjustment": "تعديل المخزون",
        "Stock Transfer": "نقل المخزون",
        "Stock Count": "جرد المخزون",
        "Movement Type": "نوع الحركة",
        "Reference": "المرجع",
        "Reason": "السبب",
        
        # التنبيهات والإشعارات
        "Low Stock Alert": "تنبيه مخزون منخفض",
        "Out of Stock Alert": "تنبيه نفاد المخزون",
        "Expiry Alert": "تنبيه انتهاء الصلاحية",
        "Overstock Alert": "تنبيه مخزون زائد",
        "Notification": "إشعار",
        "Mark as Read": "تحديد كمقروء",
        "Mark All as Read": "تحديد الكل كمقروء",
        "Clear All": "مسح الكل",
        
        # إدارة المستخدمين
        "User Management": "إدارة المستخدمين",
        "Add User": "إضافة مستخدم",
        "Edit User": "تعديل المستخدم",
        "User Details": "تفاصيل المستخدم",
        "Permissions": "الصلاحيات",
        "User Role": "دور المستخدم",
        "Status": "الحالة",
        "Last Login": "آخر دخول",
        "Date Joined": "تاريخ الانضمام",
        "Change Password": "تغيير كلمة المرور",
        "Reset Password": "إعادة تعيين كلمة المرور",
        
        # الإعدادات
        "General Settings": "الإعدادات العامة",
        "Company Information": "معلومات الشركة",
        "Company Name": "اسم الشركة",
        "Company Logo": "شعار الشركة",
        "Tax Settings": "إعدادات الضريبة",
        "Currency": "العملة",
        "Language": "اللغة",
        "Time Zone": "المنطقة الزمنية",
        "Backup": "نسخ احتياطي",
        "Restore": "استعادة",
        "System Preferences": "تفضيلات النظام",
        
        # الإجراءات السريعة
        "Quick Sale": "بيع سريع",
        "Quick Purchase": "شراء سريع",
        "Quick Add Product": "إضافة منتج سريع",
        "Barcode Scanner": "ماسح الباركود",
        "POS": "نقطة البيع",
        
        # المصطلحات المالية
        "Revenue": "الإيرادات",
        "Profit": "الربح",
        "Loss": "الخسارة",
        "Margin": "الهامش",
        "Commission": "العمولة",
        "Discount": "الخصم",
        "VAT": "ضريبة القيمة المضافة",
        "Net Amount": "المبلغ الصافي",
        "Gross Amount": "المبلغ الإجمالي"
    }
    
    # إنشاء ملف .po عربي شامل
    po_content = '''# ترجمة عربية شاملة لنظام سبير سمارت
# حقوق الطبع والنشر (C) 2024 فريق سبير سمارت
# يتم توزيع هذا الملف تحت نفس رخصة حزمة سبير سمارت.
#
msgid ""
msgstr ""
"Project-Id-Version: SpareSmart 1.0\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2025-01-15 14:00+0200\\n"
"PO-Revision-Date: 2025-01-15 14:00+0200\\n"
"Last-Translator: فريق سبير سمارت\\n"
"Language: ar\\n"
"Language-Team: العربية\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 ? 4 : 5;\\n"

'''
    
    # إضافة جميع الترجمات إلى ملف .po
    for msgid, msgstr in comprehensive_arabic_translations.items():
        po_content += f'msgid "{msgid}"\n'
        po_content += f'msgstr "{msgstr}"\n\n'
    
    # كتابة ملف .po
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(po_content)
    print("تم إنشاء ملف الترجمة العربية الشامل (.po)")
    
    # إنشاء ملف .mo
    create_comprehensive_arabic_mo(comprehensive_arabic_translations, 'locale/ar/LC_MESSAGES/django.mo')
    
    print("تم إنشاء النظام العربي بالكامل بنجاح!")
    print(f"عدد الترجمات: {len(comprehensive_arabic_translations)}")

if __name__ == '__main__':
    main()
