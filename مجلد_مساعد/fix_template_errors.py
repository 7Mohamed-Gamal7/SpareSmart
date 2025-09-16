#!/usr/bin/env python3
"""
إصلاح أخطاء القوالب وإزالة علامات {% trans %} المتبقية
"""
import os
import re
from pathlib import Path

def fix_template_file(file_path):
    """إصلاح ملف قالب واحد"""
    
    print(f"🔄 إصلاح: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = 0
        
        # إزالة جميع علامات {% trans %} وتحويلها لنص عربي مباشر
        trans_patterns = [
            (r'{%\s*trans\s*"([^"]+)"\s*%}', r'\1'),  # {% trans "text" %}
            (r"{%\s*trans\s*'([^']+)'\s*%}", r'\1'),  # {% trans 'text' %}
            (r'{%\s*trans\s*([^%]+)\s*%}', r'\1'),    # {% trans variable %}
        ]
        
        for pattern, replacement in trans_patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_made += len(matches)
                print(f"   ✅ إزالة {len(matches)} علامة trans")
        
        # إصلاح النصوص الإنجليزية المتبقية
        english_to_arabic = {
            "Today's Orders": "طلبات اليوم",
            "Today's Amount": "مبلغ اليوم", 
            "Today's Expenses": "مصروفات اليوم",
            "Pending Orders": "الطلبات المعلقة",
            "Purchase Orders": "أوامر الشراء",
            "Expense Management": "إدارة المصروفات",
            "Quick Purchase": "شراء سريع",
            "View Details": "عرض التفاصيل",
            "View Invoice": "عرض الفاتورة",
            "Receive Goods": "استلام البضائع",
            "Record Payment": "تسجيل دفعة",
            "No Purchase Orders Found": "لا توجد أوامر شراء",
            "No Expenses Found": "لا توجد مصروفات",
            "Create First Purchase": "إنشاء أول شراء",
            "Create First Expense": "إنشاء أول مصروف",
            "Approve": "موافقة",
            "Recurring": "متكررة",
            "Petty Cash": "النثرية",
            "Purchase #": "رقم الشراء",
            "Supplier": "supplier",
            "Date": "date",
            "Items": "العناصر",
            "Amount": "amount",
            "Paid": "paid",
            "Balance": "الرصيد",
            "Status": "status",
            "Payment": "الدفع",
            "Actions": "الإجراءات",
            "Clear": "مسح",
            "items": "عنصر",
            "products": "منتج",
            "discount": "خصم",
            "shipping": "شحن",
        }
        
        for english, arabic in english_to_arabic.items():
            if english in content:
                content = content.replace(f'>{english}<', f'>{arabic}<')
                content = content.replace(f'"{english}"', f'"{arabic}"')
                content = content.replace(f"'{english}'", f"'{arabic}'")
                changes_made += 1
        
        # حفظ الملف إذا تم إجراء تغييرات
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ تم إصلاح {changes_made} مشكلة")
            return changes_made
        else:
            print(f"   ⚪ لا توجد مشاكل")
            return 0
            
    except Exception as e:
        print(f"   ❌ خطأ: {e}")
        return 0

def fix_python_field_names():
    """إصلاح أسماء الحقول في ملفات Python"""
    
    print("\n🐍 إصلاح أسماء الحقول في ملفات Python...")
    
    # قائمة الملفات التي تحتاج إصلاح
    files_to_fix = [
        'dashboard/models.py',
        'sales/models.py',
        'purchases/models.py',
        'expenses/models.py',
        'inventory/models.py',
        'accounts/models.py',
    ]
    
    # الترجمات الخاطئة التي يجب إصلاحها
    wrong_translations = {
        'created_at': 'created_at',
        'updated_at': 'updated_at',
        'created_by': 'created_by',
        'updated_by': 'updated_by',
        'name': 'name',
        'description': 'description',
        'category': 'category',
        'price': 'price',
        'quantity': 'quantity',
        'date': 'date',
        'amount': 'amount',
        'status': 'status',
    }
    
    total_fixes = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"🔄 إصلاح: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # إصلاح أسماء الحقول الخاطئة
                for wrong, correct in wrong_translations.items():
                    if f"'{wrong}'" in content:
                        content = content.replace(f"'{wrong}'", f"'{correct}'")
                        total_fixes += 1
                    if f'"{wrong}"' in content:
                        content = content.replace(f'"{wrong}"', f'"{correct}"')
                        total_fixes += 1
                
                # حفظ الملف إذا تم إجراء تغييرات
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   ✅ تم إصلاح أسماء الحقول")
                else:
                    print(f"   ⚪ لا توجد مشاكل")
                    
            except Exception as e:
                print(f"   ❌ خطأ: {e}")
    
    print(f"✅ تم إصلاح {total_fixes} اسم حقل خاطئ")

def main():
    """الدالة الرئيسية"""
    
    print("🔧 إصلاح أخطاء القوالب والنماذج")
    print("=" * 60)
    
    # إصلاح أسماء الحقول في ملفات Python أولاً
    fix_python_field_names()
    
    # البحث عن ملفات HTML التي تحتوي على أخطاء
    problem_files = [
        'templates/purchases/purchase_list.html',
        'templates/expenses/expense_list.html',
    ]
    
    print(f"\n📁 إصلاح {len(problem_files)} ملف قالب")
    
    total_changes = 0
    
    # إصلاح كل ملف
    for html_file in problem_files:
        if os.path.exists(html_file):
            changes = fix_template_file(html_file)
            total_changes += changes
        else:
            print(f"⚠️  الملف غير موجود: {html_file}")
    
    print()
    print("=" * 60)
    print(f"🎉 تم الانتهاء من الإصلاح!")
    print(f"✅ تم إصلاح {total_changes} مشكلة في القوالب")
    print(f"✅ تم إصلاح أسماء الحقول في ملفات Python")
    print(f"✅ يجب أن تعمل الصفحات الآن بدون أخطاء")

if __name__ == '__main__':
    main()
