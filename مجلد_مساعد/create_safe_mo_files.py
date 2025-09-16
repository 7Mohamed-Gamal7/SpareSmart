#!/usr/bin/env python3
"""
Create safe .mo files that Django can load without Unicode errors
"""
import os
import struct

def create_safe_mo_file(translations, mo_path):
    """Create a safe .mo file that Django can load"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    if not translations:
        # Create empty .mo file
        with open(mo_path, 'wb') as f:
            # Write minimal .mo file header
            f.write(struct.pack('<I', 0x950412de))  # Magic number
            f.write(struct.pack('<I', 0))           # Version
            f.write(struct.pack('<I', 0))           # Number of strings
            f.write(struct.pack('<I', 28))          # Offset of key table
            f.write(struct.pack('<I', 28))          # Offset of value table
            f.write(struct.pack('<I', 0))           # Hash table size
            f.write(struct.pack('<I', 28))          # Offset of hash table
        return
    
    # Convert to bytes with proper encoding
    keys = []
    values = []
    
    # Add empty string entry (required for .mo files)
    keys.append(b'')
    values.append(b'Content-Type: text/plain; charset=UTF-8\n')
    
    for msgid, msgstr in translations.items():
        try:
            # Encode both key and value as UTF-8
            key_bytes = msgid.encode('utf-8')
            value_bytes = msgstr.encode('utf-8')
            keys.append(key_bytes)
            values.append(value_bytes)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(f"Skipping problematic translation: {msgid} -> {msgstr} ({e})")
            continue
    
    if len(keys) <= 1:  # Only empty string
        print("No valid translations found, creating empty .mo file")
        create_safe_mo_file({}, mo_path)
        return
    
    # Calculate offsets
    koffsets = []
    voffsets = []
    
    # Start after header and offset tables
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        koffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        voffsets.append((offset, len(value)))
        offset += len(value)
    
    # Write .mo file
    try:
        with open(mo_path, 'wb') as f:
            # Write header
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
                
        print(f"Successfully created {mo_path} with {len(keys)-1} translations")
        
    except Exception as e:
        print(f"Error creating .mo file {mo_path}: {e}")
        # Create empty .mo file as fallback
        create_safe_mo_file({}, mo_path)

def main():
    print("Creating safe .mo files for Django...")
    
    # Create directories
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    
    # Basic safe Arabic translations (only essential ones)
    safe_arabic_translations = {
        "SpareSmart": "سبير سمارت",
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
        "Products": "المنتجات",
        "Categories": "الفئات",
        "Customers": "العملاء",
        "Add": "إضافة",
        "Edit": "تعديل",
        "Delete": "حذف",
        "Save": "حفظ",
        "Cancel": "إلغاء",
        "Search": "بحث",
        "Welcome back": "مرحباً بعودتك",
        "Today's Sales": "مبيعات اليوم",
        "Total Revenue": "إجمالي الإيرادات",
        "Low Stock Items": "المنتجات منخفضة المخزون"
    }
    
    # Create Arabic .mo file
    create_safe_mo_file(safe_arabic_translations, 'locale/ar/LC_MESSAGES/django.mo')
    
    # Create English .mo file (identity mapping)
    english_translations = {k: k for k in safe_arabic_translations.keys()}
    create_safe_mo_file(english_translations, 'locale/en/LC_MESSAGES/django.mo')
    
    print("Safe .mo files created successfully!")

if __name__ == '__main__':
    main()
