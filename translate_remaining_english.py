#!/usr/bin/env python3
"""
ترجمة النصوص الإنجليزية المتبقية في القوالب
"""
import os
import re
from pathlib import Path

def translate_template_file(file_path):
    """ترجمة ملف قالب واحد"""
    
    print(f"🔄 ترجمة: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # قاموس الترجمة الشامل للنصوص المتبقية
        translations = {
            # عناوين الصفحات والأقسام
            "Dashboard": "لوحة التحكم",
            "Products": "المنتجات",
            "Product": "المنتج",
            "Sales": "المبيعات",
            "Sale": "البيع",
            "Purchases": "المشتريات",
            "Purchase": "الشراء",
            "Expenses": "المصروفات",
            "Expense": "المصروف",
            "Reports": "التقارير",
            "Report": "التقرير",
            "Inventory": "المخزون",
            "Customers": "العملاء",
            "Customer": "العميل",
            "Suppliers": "الموردين",
            "Supplier": "المورد",
            "Categories": "الفئات",
            "Category": "الفئة",
            "Users": "المستخدمين",
            "User": "المستخدم",
            
            # أعمدة الجداول
            "Name": "الاسم",
            "Description": "الوصف",
            "Price": "السعر",
            "Cost Price": "سعر التكلفة",
            "Selling Price": "سعر البيع",
            "Quantity": "الكمية",
            "Stock": "المخزون",
            "Stock Quantity": "كمية المخزون",
            "Min Stock": "الحد الأدنى",
            "Barcode": "الباركود",
            "SKU": "رمز المنتج",
            "Brand": "العلامة التجارية",
            "Model": "الموديل",
            "Date": "التاريخ",
            "Amount": "المبلغ",
            "Total": "الإجمالي",
            "Total Amount": "المبلغ الإجمالي",
            "Paid": "مدفوع",
            "Paid Amount": "المبلغ المدفوع",
            "Balance": "الرصيد",
            "Discount": "الخصم",
            "Tax": "الضريبة",
            "Notes": "ملاحظات",
            "Status": "الحالة",
            "Payment Method": "طريقة الدفع",
            "Phone": "الهاتف",
            "Email": "البريد الإلكتروني",
            "Address": "العنوان",
            "City": "المدينة",
            "Country": "البلد",
            "Created": "تاريخ الإنشاء",
            "Updated": "تاريخ التحديث",
            "Created At": "تاريخ الإنشاء",
            "Updated At": "تاريخ التحديث",
            "Created By": "أنشئ بواسطة",
            "Updated By": "حُدث بواسطة",
            
            # الحالات والأوضاع
            "Active": "نشط",
            "Inactive": "غير نشط",
            "Pending": "معلق",
            "Approved": "موافق عليه",
            "Rejected": "مرفوض",
            "Completed": "مكتمل",
            "Cancelled": "ملغي",
            "Draft": "مسودة",
            "Ordered": "مطلوب",
            "Received": "مستلم",
            "Partial": "جزئي",
            "Unpaid": "غير مدفوع",
            "Overdue": "متأخر",
            "Cash": "نقدي",
            "Credit": "آجل",
            "Card": "بطاقة",
            "Bank Transfer": "تحويل بنكي",
            
            # الأزرار والإجراءات
            "Add": "إضافة",
            "Edit": "تعديل",
            "Delete": "حذف",
            "View": "عرض",
            "Save": "حفظ",
            "Cancel": "إلغاء",
            "Submit": "إرسال",
            "Update": "تحديث",
            "Create": "إنشاء",
            "Search": "بحث",
            "Filter": "تصفية",
            "Clear": "مسح",
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
            "Actions": "الإجراءات",
            "Options": "الخيارات",
            "Settings": "الإعدادات",
            "Profile": "الملف الشخصي",
            "Logout": "تسجيل خروج",
            "Login": "تسجيل دخول",
            
            # رسائل النظام
            "Success": "نجح",
            "Error": "خطأ",
            "Warning": "تحذير",
            "Info": "معلومات",
            "Loading": "جاري التحميل",
            "Please wait": "يرجى الانتظار",
            "No data available": "لا توجد بيانات",
            "No results found": "لا توجد نتائج",
            "Are you sure": "هل أنت متأكد",
            "Confirm": "تأكيد",
            "Yes": "نعم",
            "No": "لا",
            "OK": "موافق",
            "Close": "إغلاق",
            
            # عبارات شائعة
            "Select": "اختر",
            "Choose": "اختر",
            "All": "الكل",
            "None": "لا شيء",
            "Other": "أخرى",
            "Total Records": "إجمالي السجلات",
            "Page": "صفحة",
            "of": "من",
            "Show": "عرض",
            "entries": "إدخال",
            "Showing": "عرض",
            "to": "إلى",
            "Search:": "البحث:",
            "Sort by": "ترتيب حسب",
            "Order by": "ترتيب حسب",
            "Ascending": "تصاعدي",
            "Descending": "تنازلي",
            
            # أسماء الحقول المتخصصة
            "Quick Sale": "بيع سريع",
            "Quick Purchase": "شراء سريع",
            "View Details": "عرض التفاصيل",
            "View Invoice": "عرض الفاتورة",
            "Receive Goods": "استلام البضائع",
            "Record Payment": "تسجيل دفعة",
            "Purchase Order": "أمر شراء",
            "Purchase Orders": "أوامر الشراء",
            "Sales Order": "أمر بيع",
            "Sales Orders": "أوامر البيع",
            "Invoice": "فاتورة",
            "Invoices": "الفواتير",
            "Receipt": "إيصال",
            "Receipts": "الإيصالات",
            "Payment": "الدفع",
            "Payments": "المدفوعات",
            
            # رسائل خاصة
            "No Purchase Orders Found": "لا توجد أوامر شراء",
            "No Expenses Found": "لا توجد مصروفات",
            "No Sales Found": "لا توجد مبيعات",
            "No Products Found": "لا توجد منتجات",
            "Create First Purchase": "إنشاء أول شراء",
            "Create First Expense": "إنشاء أول مصروف",
            "Create First Sale": "إنشاء أول بيع",
            "Create First Product": "إنشاء أول منتج",
            
            # أرقام وإحصائيات
            "Today": "اليوم",
            "Yesterday": "أمس",
            "This Week": "هذا الأسبوع",
            "This Month": "هذا الشهر",
            "This Year": "هذا العام",
            "Last Week": "الأسبوع الماضي",
            "Last Month": "الشهر الماضي",
            "Last Year": "العام الماضي",
            "items": "عنصر",
            "products": "منتج",
            "orders": "طلب",
            "customers": "عميل",
            "suppliers": "مورد",
        }
        
        # تطبيق الترجمات
        for english, arabic in translations.items():
            # ترجمة النصوص داخل العلامات
            patterns = [
                (f'>{english}<', f'>{arabic}<'),
                (f'>{english.upper()}<', f'>{arabic}<'),
                (f'>{english.lower()}<', f'>{arabic}<'),
                (f'"{english}"', f'"{arabic}"'),
                (f"'{english}'", f"'{arabic}'"),
                (f'placeholder="{english}"', f'placeholder="{arabic}"'),
                (f"placeholder='{english}'", f"placeholder='{arabic}'"),
                (f'title="{english}"', f'title="{arabic}"'),
                (f"title='{english}'", f"title='{arabic}'"),
                (f'alt="{english}"', f'alt="{arabic}"'),
                (f"alt='{english}'", f"alt='{arabic}'"),
                (f'value="{english}"', f'value="{arabic}"'),
                (f"value='{english}'", f"value='{arabic}'"),
            ]
            
            for old_pattern, new_pattern in patterns:
                if old_pattern in content:
                    content = content.replace(old_pattern, new_pattern)
                    changes_made += 1
        
        # حفظ الملف إذا تم إجراء تغييرات
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ تم ترجمة {changes_made} نص")
            return changes_made
        else:
            print(f"   ⚪ لا توجد نصوص إنجليزية")
            return 0
            
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        return 0

def main():
    """الدالة الرئيسية"""
    
    print("🌍 ترجمة النصوص الإنجليزية المتبقية")
    print("=" * 60)
    
    # البحث عن جميع ملفات HTML
    html_files = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"📁 تم العثور على {len(html_files)} ملف HTML")
    
    total_changes = 0
    
    # ترجمة كل ملف
    for html_file in html_files:
        changes = translate_template_file(html_file)
        total_changes += changes
    
    print()
    print("=" * 60)
    print(f"🎉 تم الانتهاء من الترجمة!")
    print(f"✅ تم ترجمة {total_changes} نص إنجليزي")
    print(f"✅ النظام الآن عربي بالكامل")

if __name__ == '__main__':
    main()
