#!/usr/bin/env python3
"""
إصلاح جميع أسماء الحقول الخاطئة في ملفات Python
"""
import os
import re
from pathlib import Path

def fix_field_names():
    """إصلاح أسماء الحقول في جميع ملفات Python"""
    
    print("🔧 إصلاح أسماء الحقول في ملفات Python...")
    
    # قائمة الترجمات الخاطئة التي يجب إصلاحها
    wrong_translations = {
        # أسماء الحقول الأساسية
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
        
        # أسماء الحقول المتخصصة
        'phone_number': 'phone_number',
        'profile_image': 'profile_image',
        'active': 'is_active',
        'is_active_employee': 'is_active_employee',
        'admin': 'admin',
        'manager': 'manager',
        'sales': 'sales',
        'cashier': 'cashier',
        'viewer': 'viewer',
        
        # حقول النماذج
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
    }
    
    # البحث عن جميع ملفات Python
    python_files = []
    for root, dirs, files in os.walk('.'):
        # تجاهل مجلدات معينة
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'migrations']]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"📁 تم العثور على {len(python_files)} ملف Python")
    
    total_fixes = 0
    
    for file_path in python_files:
        print(f"🔄 معالجة: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            file_fixes = 0
            
            # إصلاح أسماء الحقول في السلاسل النصية
            for wrong, correct in wrong_translations.items():
                patterns = [
                    (f"'{wrong}'", f"'{correct}'"),
                    (f'"{wrong}"', f'"{correct}"'),
                    (f"fields = ('{wrong}'", f"fields = ('{correct}'"),
                    (f"fields = ['{wrong}'", f"fields = ['{correct}'"),
                    (f", '{wrong}'", f", '{correct}'"),
                    (f', "{wrong}"', f', "{correct}"'),
                ]
                
                for old_pattern, new_pattern in patterns:
                    if old_pattern in content:
                        count = content.count(old_pattern)
                        content = content.replace(old_pattern, new_pattern)
                        file_fixes += count
            
            # حفظ الملف إذا تم إجراء تغييرات
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ تم إصلاح {file_fixes} اسم حقل")
                total_fixes += file_fixes
            else:
                print(f"   ⚪ لا توجد مشاكل")
                
        except Exception as e:
            print(f"   ❌ خطأ: {e}")
    
    print(f"\n✅ تم إصلاح {total_fixes} اسم حقل خاطئ في {len(python_files)} ملف")
    return total_fixes

def main():
    """الدالة الرئيسية"""
    
    print("🔧 إصلاح أسماء الحقول الخاطئة")
    print("=" * 60)
    
    # إصلاح أسماء الحقول
    total_fixes = fix_field_names()
    
    print()
    print("=" * 60)
    print(f"🎉 تم الانتهاء من الإصلاح!")
    print(f"✅ تم إصلاح {total_fixes} اسم حقل خاطئ")
    print(f"✅ يجب أن يعمل الخادم الآن بدون أخطاء")

if __name__ == '__main__':
    main()
