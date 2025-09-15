#!/usr/bin/env python3
"""
إنشاء ملف .mo عربي يعمل مع Django
"""
import os
import subprocess
import sys

def create_working_mo():
    """إنشاء ملف .mo باستخدام msgfmt"""
    
    # التأكد من وجود ملف .po
    po_file = 'locale/ar/LC_MESSAGES/django.po'
    mo_file = 'locale/ar/LC_MESSAGES/django.mo'
    
    if not os.path.exists(po_file):
        print(f"ملف .po غير موجود: {po_file}")
        return False
    
    try:
        # محاولة استخدام msgfmt إذا كان متوفراً
        result = subprocess.run(['msgfmt', '-o', mo_file, po_file], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"تم إنشاء {mo_file} بنجاح باستخدام msgfmt")
            return True
        else:
            print(f"فشل msgfmt: {result.stderr}")
    except FileNotFoundError:
        print("msgfmt غير متوفر، سأستخدم Django")
    
    # استخدام Django لإنشاء ملف .mo
    try:
        # تعطيل LOCALE_PATHS مؤقتاً في الإعدادات
        settings_file = 'sparesmart/settings.py'
        
        # قراءة الإعدادات الحالية
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings_content = f.read()
        
        # تفعيل LOCALE_PATHS
        updated_content = settings_content.replace(
            '# LOCALE_PATHS = [',
            'LOCALE_PATHS = ['
        ).replace(
            '#     BASE_DIR / \'locale\',',
            '    BASE_DIR / \'locale\','
        ).replace(
            '# ]',
            ']'
        )
        
        # كتابة الإعدادات المحدثة
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("تم تفعيل LOCALE_PATHS")
        
        # تشغيل compilemessages
        result = subprocess.run([sys.executable, 'manage.py', 'compilemessages'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("تم إنشاء ملف .mo بنجاح باستخدام Django")
            return True
        else:
            print(f"فشل Django compilemessages: {result.stderr}")
            
            # إعادة تعطيل LOCALE_PATHS في حالة الفشل
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(settings_content)
            print("تم إعادة تعطيل LOCALE_PATHS")
            
    except Exception as e:
        print(f"خطأ في إنشاء ملف .mo: {e}")
        
        # إعادة تعطيل LOCALE_PATHS في حالة الخطأ
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(settings_content)
            print("تم إعادة تعطيل LOCALE_PATHS")
        except:
            pass
    
    return False

def create_minimal_po():
    """إنشاء ملف .po بسيط للاختبار"""
    
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    
    # ترجمات أساسية فقط
    basic_translations = {
        "Dashboard": "لوحة التحكم",
        "SpareSmart": "سبير سمارت",
        "Products": "المنتجات",
        "Inventory": "المخزون",
        "Sales": "المبيعات",
        "Welcome back": "مرحباً بعودتك",
        "Login": "تسجيل الدخول",
        "Username": "اسم المستخدم",
        "Password": "كلمة المرور",
        "Add Product": "إضافة منتج",
        "Edit": "تعديل",
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "Search": "بحث",
        "Actions": "الإجراءات",
        "Name": "الاسم",
        "Price": "السعر",
        "Stock": "المخزون",
        "Category": "الفئة",
        "Brand": "العلامة التجارية"
    }
    
    po_content = '''# ترجمة عربية أساسية لنظام سبير سمارت
msgid ""
msgstr ""
"Project-Id-Version: SpareSmart 1.0\\n"
"Language: ar\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"

'''
    
    for msgid, msgstr in basic_translations.items():
        po_content += f'msgid "{msgid}"\n'
        po_content += f'msgstr "{msgstr}"\n\n'
    
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(po_content)
    
    print("تم إنشاء ملف .po أساسي")

def main():
    print("إنشاء ملف ترجمة عربي يعمل مع Django...")
    
    # إنشاء ملف .po بسيط
    create_minimal_po()
    
    # إنشاء ملف .mo
    if create_working_mo():
        print("✅ تم إنشاء نظام الترجمة العربي بنجاح!")
    else:
        print("❌ فشل في إنشاء ملف .mo")

if __name__ == '__main__':
    main()
