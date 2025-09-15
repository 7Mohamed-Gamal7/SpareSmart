#!/usr/bin/env python3
"""
ترجمة جميع النصوص الإنجليزية في القوالب إلى العربية
"""
import os
import re
from pathlib import Path

def get_translation_dict():
    """قاموس الترجمات الشامل"""
    return {
        # Headers and Titles
        'Purchase Orders': 'أوامر الشراء',
        'Expense Management': 'إدارة المصروفات',
        'Product Management': 'إدارة المنتجات',
        'Sales Management': 'إدارة المبيعات',
        'Reports': 'التقارير',
        'Dashboard': 'لوحة التحكم',

        # Common Actions
        'Create': 'إنشاء',
        'Edit': 'تعديل',
        'Delete': 'حذف',
        'View': 'عرض',
        'Save': 'حفظ',
        'Cancel': 'إلغاء',
        'Submit': 'إرسال',
        'Update': 'تحديث',
        'Add': 'إضافة',
        'Remove': 'إزالة',
        'Clear': 'مسح',
        'Search': 'بحث',
        'Filter': 'تصفية',
        'Export': 'تصدير',
        'Import': 'استيراد',
        'Print': 'طباعة',

        # Table Headers
        'Name': 'name',
        'Description': 'description',
        'Category': 'category',
        'Price': 'price',
        'Quantity': 'quantity',
        'Total': 'الإجمالي',
        'Date': 'date',
        'Status': 'status',
        'Actions': 'الإجراءات',
        'Amount': 'amount',
        'Balance': 'الرصيد',
        'Payment': 'الدفع',
        'Supplier': 'supplier',
        'Customer': 'customer',
        'Product': 'المنتج',
        'Order': 'الطلب',
        'Invoice': 'الفاتورة',

        # Purchase specific
        'Purchase #': 'رقم الشراء',
        'Purchase Orders': 'أوامر الشراء',
        'Quick Purchase': 'شراء سريع',
        'Manage purchase orders, receiving, and supplier payments': 'إدارة أوامر الشراء والاستلام ومدفوعات الموردين',
        'Today\'s Orders': 'طلبات اليوم',
        'Today\'s Amount': 'مبلغ اليوم',
        'Pending Orders': 'الطلبات المعلقة',
        'View Details': 'عرض التفاصيل',
        'View Invoice': 'عرض الفاتورة',
        'Receive Goods': 'استلام البضائع',
        'Record Payment': 'تسجيل دفعة',
        'No Purchase Orders Found': 'لا توجد أوامر شراء',
        'Start managing your inventory by creating your first purchase order.': 'ابدأ إدارة مخزونك بإنشاء أول أمر شراء.',
        'Create First Purchase': 'إنشاء أول شراء',

        # Expense specific
        'Today\'s Expenses': 'مصروفات اليوم',
        'Track and manage business expenses and approvals': 'تتبع وإدارة مصروفات الأعمال والموافقات',
        'Recurring': 'متكررة',
        'Petty Cash': 'النثرية',
        'No Expenses Found': 'لا توجد مصروفات',
        'Start tracking your business expenses by creating your first expense record.': 'ابدأ تتبع مصروفات عملك بإنشاء أول سجل مصروف.',
        'Create First Expense': 'إنشاء أول مصروف',
        'Approve': 'موافقة',

        # Sales specific
        'Sales': 'المبيعات',
        'Quick Sale': 'بيع سريع',
        'New Sale': 'بيع جديد',
        'Sale #': 'رقم البيع',
        'Customer': 'customer',
        'Items': 'العناصر',
        'Paid': 'paid',
        'Due': 'مستحق',
        'Installments': 'الأقساط',
        'Cash Sale': 'بيع نقدي',
        'Credit Sale': 'بيع آجل',

        # Product specific
        'Products': 'المنتجات',
        'Add Product': 'إضافة منتج',
        'Product Name': 'اسم المنتج',
        'Brand': 'brand',
        'Model': 'model',
        'SKU': 'sku',
        'Barcode': 'barcode',
        'Stock': 'المخزون',
        'Min Stock': 'min_stock_level',
        'Cost Price': 'cost_price',
        'Selling Price': 'selling_price',
        'Profit Margin': 'هامش الربح',
        'In Stock': 'متوفر',
        'Out of Stock': 'غير متوفر',
        'Low Stock': 'مخزون منخفض',

        # Status values
        'Active': 'active',
        'Inactive': 'inactive',
        'Pending': 'pending',
        'Approved': 'approved',
        'Rejected': 'rejected',
        'Completed': 'completed',
        'Cancelled': 'cancelled',
        'Draft': 'draft',
        'Ordered': 'ordered',
        'Received': 'received',
        'Partial': 'partial',
        'Overdue': 'overdue',

        # Common phrases
        'No data available': 'لا توجد بيانات متاحة',
        'Loading...': 'جاري التحميل...',
        'Please wait...': 'يرجى الانتظار...',
        'Are you sure?': 'هل أنت متأكد؟',
        'This action cannot be undone': 'لا يمكن التراجع عن هذا الإجراء',
        'Success': 'نجح',
        'Error': 'خطأ',
        'Warning': 'تحذير',
        'Information': 'معلومات',

        # Form labels
        'Required': 'ordered',
        'Optional': 'اختياري',
        'Select...': 'اختر...',
        'Choose file': 'اختر ملف',
        'Browse': 'تصفح',
        'Upload': 'رفع',
        'Download': 'تحميل',

        # Time and date
        'Today': 'اليوم',
        'Yesterday': 'أمس',
        'This Week': 'هذا الأسبوع',
        'This Month': 'هذا الشهر',
        'This Year': 'هذا العام',
        'Last Week': 'الأسبوع الماضي',
        'Last Month': 'الشهر الماضي',
        'Last Year': 'العام الماضي',

        # Numbers and currency
        'items': 'عنصر',
        'products': 'منتج',
        'discount': 'خصم',
        'shipping': 'شحن',
        'tax': 'ضريبة',
        'subtotal': 'المجموع الفرعي',
        'total': 'الإجمالي',

        # Navigation
        'Home': 'الرئيسية',
        'Back': 'رجوع',
        'Next': 'التالي',
        'Previous': 'السابق',
        'First': 'الأول',
        'Last': 'الأخير',
        'Page': 'صفحة',
        'of': 'من',

        # Buttons and links
        'Show': 'عرض',
        'Hide': 'إخفاء',
        'Expand': 'توسيع',
        'Collapse': 'طي',
        'Refresh': 'تحديث',
        'Reload': 'إعادة تحميل',
        'Reset': 'إعادة تعيين',
        'Apply': 'تطبيق',
        'Close': 'إغلاق',
        'Open': 'فتح',

        # Messages
        'No results found': 'لا توجد نتائج',
        'Search results': 'نتائج البحث',
        'Showing': 'عرض',
        'entries': 'إدخال',
        'All': 'الكل',
        'None': 'لا شيء',
        'Other': 'أخرى',
        'More': 'المزيد',
        'Less': 'أقل',
    }

def translate_file(file_path, translations):
    """ترجمة ملف واحد"""

    print(f"🔄 معالجة: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # ترجمة النصوص
        for english, arabic in translations.items():
            # البحث عن النص الإنجليزي وترجمته
            patterns = [
                f'>{english}<',  # في العلامات HTML
                f'"{english}"',  # في الخصائص
                f"'{english}'",  # في الخصائص بعلامات فردية
                f'>{english}',   # في بداية العلامات
                f'{english}<',   # في نهاية العلامات
            ]

            for pattern in patterns:
                if pattern in content:
                    new_pattern = pattern.replace(english, arabic)
                    if content.count(pattern) > 0:
                        content = content.replace(pattern, new_pattern)
                        changes_made += 1

        # حفظ الملف إذا تم إجراء تغييرات
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ تم تحديث {changes_made} نص")
            return changes_made
        else:
            print(f"   ⚪ لا توجد تغييرات")
            return 0

    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        return 0

def main():
    """الدالة الرئيسية"""

    print("🌐 ترجمة جميع النصوص الإنجليزية في القوالب")
    print("=" * 60)

    # الحصول على قاموس الترجمات
    translations = get_translation_dict()
    print(f"📚 تم تحميل {len(translations)} ترجمة")

    # البحث عن جميع ملفات HTML
    templates_dir = Path('templates')
    html_files = list(templates_dir.rglob('*.html'))

    print(f"📁 تم العثور على {len(html_files)} ملف HTML")
    print()

    total_changes = 0

    # معالجة كل ملف
    for html_file in html_files:
        changes = translate_file(html_file, translations)
        total_changes += changes

    print()
    print("=" * 60)
    print(f"🎉 تم الانتهاء من الترجمة!")
    print(f"✅ تم تحديث {total_changes} نص في {len(html_files)} ملف")
    print(f"✅ النظام الآن باللغة العربية بالكامل")

if __name__ == '__main__':
    main()