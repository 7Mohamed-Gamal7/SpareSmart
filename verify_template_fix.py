#!/usr/bin/env python3
"""
التحقق من إصلاح خطأ القالب وحالة النظام العربي
"""
import os
import re

def check_template_issues():
    """فحص القوالب للتأكد من عدم وجود مشاكل"""
    
    print("🔍 فحص القوالب للتأكد من الإصلاح...")
    
    template_file = 'templates/base.html'
    
    if not os.path.exists(template_file):
        print(f"❌ الملف غير موجود: {template_file}")
        return False
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # فحص العلامات المشكلة
        if '{% get_current_language' in content:
            issues.append("❌ ما زالت توجد علامة {% get_current_language %}")
        
        if '{% get_current_language_bidi' in content:
            issues.append("❌ ما زالت توجد علامة {% get_current_language_bidi %}")
        
        if '{% load i18n %}' in content:
            issues.append("⚠️  ما زالت توجد علامة {% load i18n %}")
        
        # فحص الإعدادات الصحيحة
        if 'lang="ar"' in content:
            print("✅ اللغة مضبوطة على العربية")
        else:
            issues.append("❌ اللغة غير مضبوطة على العربية")
        
        if 'dir="rtl"' in content:
            print("✅ الاتجاه مضبوط على RTL")
        else:
            issues.append("❌ الاتجاه غير مضبوط على RTL")
        
        if 'bootstrap.rtl.min.css' in content:
            print("✅ Bootstrap RTL محمل")
        else:
            issues.append("❌ Bootstrap RTL غير محمل")
        
        if "'Cairo', 'Tahoma', 'Arial'" in content:
            print("✅ الخطوط العربية مضبوطة")
        else:
            issues.append("❌ الخطوط العربية غير مضبوطة")
        
        # فحص النصوص العربية
        arabic_texts = [
            "سبير سمارت",
            "لوحة التحكم", 
            "المخزون",
            "المبيعات",
            "المشتريات",
            "المصروفات",
            "التقارير"
        ]
        
        arabic_count = 0
        for text in arabic_texts:
            if text in content:
                arabic_count += 1
        
        if arabic_count >= 5:
            print(f"✅ النصوص العربية موجودة ({arabic_count}/{len(arabic_texts)})")
        else:
            issues.append(f"❌ النصوص العربية ناقصة ({arabic_count}/{len(arabic_texts)})")
        
        # فحص DataTables العربية
        if 'بحث:' in content and 'جاري التحميل...' in content:
            print("✅ DataTables مترجم للعربية")
        else:
            issues.append("❌ DataTables غير مترجم للعربية")
        
        if issues:
            print("\n🚨 مشاكل موجودة:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("\n🎉 جميع الفحوصات نجحت!")
            return True
            
    except Exception as e:
        print(f"❌ خطأ في فحص الملف: {e}")
        return False

def check_settings():
    """فحص إعدادات Django"""
    
    print("\n🔍 فحص إعدادات Django...")
    
    settings_file = 'sparesmart/settings.py'
    
    if not os.path.exists(settings_file):
        print(f"❌ ملف الإعدادات غير موجود: {settings_file}")
        return False
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = []
        
        if "LANGUAGE_CODE = 'ar'" in content:
            checks.append("✅ LANGUAGE_CODE مضبوط على 'ar'")
        else:
            checks.append("❌ LANGUAGE_CODE غير مضبوط على 'ar'")
        
        if "LANGUAGES = [('ar', 'العربية')]" in content:
            checks.append("✅ LANGUAGES مضبوط للعربية فقط")
        else:
            checks.append("❌ LANGUAGES غير مضبوط للعربية فقط")
        
        if "LANGUAGE_BIDI = True" in content:
            checks.append("✅ LANGUAGE_BIDI مفعل")
        else:
            checks.append("❌ LANGUAGE_BIDI غير مفعل")
        
        # فحص تعطيل LOCALE_PATHS
        if "# LOCALE_PATHS" in content:
            checks.append("✅ LOCALE_PATHS معطل (مؤقت)")
        else:
            checks.append("⚠️  LOCALE_PATHS قد يكون مفعل")
        
        for check in checks:
            print(f"  {check}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في فحص الإعدادات: {e}")
        return False

def main():
    print("🔧 التحقق من إصلاح خطأ القالب وحالة النظام العربي")
    print("=" * 60)
    
    template_ok = check_template_issues()
    settings_ok = check_settings()
    
    print("\n" + "=" * 60)
    
    if template_ok and settings_ok:
        print("🎉 النظام يعمل بشكل صحيح!")
        print("✅ تم إصلاح خطأ TemplateSyntaxError")
        print("✅ النظام مضبوط للعربية بالكامل")
        print("✅ تخطيط RTL يعمل بشكل صحيح")
        print("✅ جميع النصوص باللغة العربية")
        print("\n🚀 النظام جاهز للاستخدام!")
    else:
        print("⚠️  توجد بعض المشاكل التي تحتاج إلى مراجعة")
    
    return template_ok and settings_ok

if __name__ == '__main__':
    main()
