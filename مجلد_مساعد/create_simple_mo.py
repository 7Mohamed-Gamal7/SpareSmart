#!/usr/bin/env python3
"""
Create simple .mo files with basic translations to test language switching
"""
import struct
import os

def create_simple_mo_file(translations, mo_path):
    """Create a simple .mo file with basic translations"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # Convert to bytes
    keys = []
    values = []
    
    for msgid, msgstr in translations.items():
        keys.append(msgid.encode('utf-8'))
        values.append(msgstr.encode('utf-8'))
    
    # Calculate offsets
    koffsets = []
    voffsets = []
    
    # Start after header (7 * 4 bytes) + string tables (8 bytes per string * 2 tables)
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        koffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        voffsets.append((offset, len(value)))
        offset += len(value)
    
    # Write .mo file
    with open(mo_path, 'wb') as f:
        # Magic number (little endian)
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of strings
        f.write(struct.pack('<I', len(keys)))
        # Offset of key table
        f.write(struct.pack('<I', 7 * 4))
        # Offset of value table
        f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))
        # Hash table size (0 = no hash table)
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 0))
        
        # Write key table
        for offset, length in koffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write value table
        for offset, length in voffsets:
            f.write(struct.pack('<II', length, offset))
        
        # Write keys
        for key in keys:
            f.write(key)
        
        # Write values
        for value in values:
            f.write(value)

def main():
    print("Creating simple .mo files for testing...")
    
    # Basic English translations
    en_translations = {
        "Dashboard": "Dashboard",
        "Inventory": "Inventory",
        "Sales": "Sales",
        "Purchases": "Purchases",
        "Expenses": "Expenses",
        "Reports": "Reports",
        "Settings": "Settings",
        "Profile": "Profile",
        "Logout": "Logout",
        "SpareSmart": "SpareSmart",
        "SpareSmart - Spare Parts Management": "SpareSmart - Spare Parts Management"
    }
    
    # Basic Arabic translations
    ar_translations = {
        "Dashboard": "لوحة التحكم",
        "Inventory": "المخزون",
        "Sales": "المبيعات",
        "Purchases": "المشتريات",
        "Expenses": "المصروفات",
        "Reports": "التقارير",
        "Settings": "الإعدادات",
        "Profile": "الملف الشخصي",
        "Logout": "تسجيل الخروج",
        "SpareSmart": "سبير سمارت",
        "SpareSmart - Spare Parts Management": "سبير سمارت - إدارة قطع الغيار"
    }
    
    # Create English .mo file
    en_mo_path = 'locale/en/LC_MESSAGES/django.mo'
    create_simple_mo_file(en_translations, en_mo_path)
    print(f"Created {en_mo_path} with {len(en_translations)} translations")
    
    # Create Arabic .mo file
    ar_mo_path = 'locale/ar/LC_MESSAGES/django.mo'
    create_simple_mo_file(ar_translations, ar_mo_path)
    print(f"Created {ar_mo_path} with {len(ar_translations)} translations")
    
    print("Done!")

if __name__ == '__main__':
    main()
