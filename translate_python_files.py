#!/usr/bin/env python3
"""
ترجمة النصوص في ملفات Python (models, views, forms)
"""
import os
import re
from pathlib import Path

def get_python_translations():
    """قاموس ترجمات ملفات Python"""
    return {
        # Model field labels and help texts
        'verbose_name': {
            'Product': 'منتج',
            'Products': 'المنتجات',
            'Category': 'فئة',
            'Categories': 'الفئات',
            'Sale': 'بيع',
            'Sales': 'المبيعات',
            'Purchase': 'شراء',
            'Purchases': 'المشتريات',
            'Expense': 'مصروف',
            'Expenses': 'المصروفات',
            'Customer': 'عميل',
            'Customers': 'العملاء',
            'Supplier': 'مورد',
            'Suppliers': 'الموردين',
            'User': 'مستخدم',
            'Users': 'المستخدمين',
            'Payment': 'دفعة',
            'Payments': 'الدفعات',
            'Invoice': 'فاتورة',
            'Invoices': 'الفواتير',
        },
        
        # Choice field options
        'choices': {
            'pending': 'pending',
            'approved': 'approved',
            'rejected': 'rejected',
            'completed': 'completed',
            'cancelled': 'cancelled',
            'active': 'active',
            'inactive': 'inactive',
            'draft': 'draft',
            'ordered': 'ordered',
            'received': 'received',
            'partial': 'partial',
            'paid': 'paid',
            'unpaid': 'unpaid',
            'overdue': 'overdue',
            'cash': 'cash',
            'credit': 'credit',
            'card': 'card',
            'bank_transfer': 'bank_transfer',
            'admin': 'admin',
            'manager': 'manager',
            'sales': 'sales',
            'cashier': 'cashier',
            'viewer': 'viewer',
        },
        
        # Form field labels
        'field_labels': {
            'name': 'name',
            'description': 'description',
            'category': 'category',
            'price': 'price',
            'cost_price': 'cost_price',
            'selling_price': 'selling_price',
            'quantity': 'quantity',
            'stock_quantity': 'stock_quantity',
            'min_stock_level': 'min_stock_level',
            'barcode': 'barcode',
            'sku': 'sku',
            'brand': 'brand',
            'model': 'model',
            'supplier': 'supplier',
            'customer': 'customer',
            'date': 'date',
            'amount': 'amount',
            'total_amount': 'total_amount',
            'paid_amount': 'paid_amount',
            'balance_amount': 'balance_amount',
            'discount': 'discount',
            'tax': 'tax',
            'notes': 'notes',
            'status': 'status',
            'payment_method': 'payment_method',
            'phone': 'phone',
            'email': 'email',
            'address': 'address',
            'city': 'city',
            'country': 'country',
            'created_at': 'created_at',
            'updated_at': 'updated_at',
            'created_by': 'created_by',
            'updated_by': 'updated_by',
        },
        
        # Help texts
        'help_texts': {
            'Enter product name': 'أدخل اسم المنتج',
            'Enter description': 'أدخل الوصف',
            'Select category': 'اختر الفئة',
            'Enter price': 'أدخل السعر',
            'Enter quantity': 'أدخل الكمية',
            'Optional notes': 'ملاحظات اختيارية',
            'Select supplier': 'اختر المورد',
            'Select customer': 'اختر العميل',
            'Enter phone number': 'أدخل رقم الهاتف',
            'Enter email address': 'أدخل عنوان البريد الإلكتروني',
            'Enter address': 'أدخل العنوان',
        },
        
        # Error messages
        'error_messages': {
            'This field is required': 'هذا الحقل مطلوب',
            'Enter a valid email': 'أدخل بريد إلكتروني صحيح',
            'Enter a valid phone number': 'أدخل رقم هاتف صحيح',
            'Price must be positive': 'يجب أن يكون السعر موجباً',
            'Quantity must be positive': 'يجب أن تكون الكمية موجبة',
            'Invalid choice': 'اختيار غير صحيح',
        },
        
        # Success messages
        'success_messages': {
            'Product created successfully': 'تم إنشاء المنتج بنجاح',
            'Product updated successfully': 'تم تحديث المنتج بنجاح',
            'Product deleted successfully': 'تم حذف المنتج بنجاح',
            'Sale created successfully': 'تم إنشاء البيع بنجاح',
            'Sale updated successfully': 'تم تحديث البيع بنجاح',
            'Purchase created successfully': 'تم إنشاء الشراء بنجاح',
            'Purchase updated successfully': 'تم تحديث الشراء بنجاح',
            'Payment recorded successfully': 'تم تسجيل الدفعة بنجاح',
            'Settings saved successfully': 'تم حفظ الإعدادات بنجاح',
        }
    }

def translate_python_file(file_path, translations):
    """ترجمة ملف Python واحد"""
    
    print(f"🔄 معالجة: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # ترجمة النصوص في ملفات Python
        all_translations = {}
        for category, trans_dict in translations.items():
            all_translations.update(trans_dict)
        
        for english, arabic in all_translations.items():
            # البحث عن النص الإنجليزي في السلاسل النصية
            patterns = [
                f'"{english}"',      # نص في علامات اقتباس مزدوجة
                f"'{english}'",      # نص في علامات اقتباس فردية
                f'_("{english}")',   # نص في دالة الترجمة
                f"_('{english}')",   # نص في دالة الترجمة بعلامات فردية
            ]
            
            for pattern in patterns:
                if pattern in content:
                    new_pattern = pattern.replace(english, arabic)
                    count = content.count(pattern)
                    if count > 0:
                        content = content.replace(pattern, new_pattern)
                        changes_made += count
        
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
    
    print("🐍 ترجمة النصوص في ملفات Python")
    print("=" * 60)
    
    # الحصول على قاموس الترجمات
    translations = get_python_translations()
    total_translations = sum(len(d) for d in translations.values())
    print(f"📚 تم تحميل {total_translations} ترجمة")
    
    # البحث عن ملفات Python في التطبيقات
    apps = ['accounts', 'inventory', 'sales', 'purchases', 'expenses', 'reports', 'dashboard']
    python_files = []
    
    for app in apps:
        app_path = Path(app)
        if app_path.exists():
            # البحث عن ملفات models.py, views.py, forms.py
            for py_file in ['models.py', 'views.py', 'forms.py', 'admin.py']:
                file_path = app_path / py_file
                if file_path.exists():
                    python_files.append(file_path)
    
    print(f"📁 تم العثور على {len(python_files)} ملف Python")
    print()
    
    total_changes = 0
    
    # معالجة كل ملف
    for py_file in python_files:
        changes = translate_python_file(py_file, translations)
        total_changes += changes
    
    print()
    print("=" * 60)
    print(f"🎉 تم الانتهاء من ترجمة ملفات Python!")
    print(f"✅ تم تحديث {total_changes} نص في {len(python_files)} ملف")
    print(f"✅ النصوص في الكود الآن باللغة العربية")

if __name__ == '__main__':
    main()
