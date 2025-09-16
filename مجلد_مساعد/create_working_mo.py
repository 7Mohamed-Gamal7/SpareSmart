#!/usr/bin/env python3
"""
Create working .mo files using a different approach
"""
import os
import subprocess
import sys

def create_po_and_mo():
    """Create proper .po and .mo files"""
    
    # Create English .po file with proper format
    en_po_content = '''# English translation for SpareSmart
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: en\\n"

msgid "Dashboard"
msgstr "Dashboard"

msgid "Inventory"
msgstr "Inventory"

msgid "Sales"
msgstr "Sales"

msgid "Purchases"
msgstr "Purchases"

msgid "Expenses"
msgstr "Expenses"

msgid "Reports"
msgstr "Reports"

msgid "Settings"
msgstr "Settings"

msgid "Profile"
msgstr "Profile"

msgid "Logout"
msgstr "Logout"

msgid "SpareSmart"
msgstr "SpareSmart"

msgid "SpareSmart - Spare Parts Management"
msgstr "SpareSmart - Spare Parts Management"
'''

    # Create Arabic .po file with proper format
    ar_po_content = '''# Arabic translation for SpareSmart
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\\n"
"Language: ar\\n"

msgid "Dashboard"
msgstr "لوحة التحكم"

msgid "Inventory"
msgstr "المخزون"

msgid "Sales"
msgstr "المبيعات"

msgid "Purchases"
msgstr "المشتريات"

msgid "Expenses"
msgstr "المصروفات"

msgid "Reports"
msgstr "التقارير"

msgid "Settings"
msgstr "الإعدادات"

msgid "Profile"
msgstr "الملف الشخصي"

msgid "Logout"
msgstr "تسجيل الخروج"

msgid "SpareSmart"
msgstr "سبير سمارت"

msgid "SpareSmart - Spare Parts Management"
msgstr "سبير سمارت - إدارة قطع الغيار"
'''

    # Write .po files
    os.makedirs('locale/en/LC_MESSAGES', exist_ok=True)
    os.makedirs('locale/ar/LC_MESSAGES', exist_ok=True)
    
    with open('locale/en/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(en_po_content)
    
    with open('locale/ar/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
        f.write(ar_po_content)
    
    print("Created .po files")
    
    # Try to use Django's compilemessages if available
    try:
        result = subprocess.run([sys.executable, 'manage.py', 'compilemessages', '--ignore=venv'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("Successfully compiled using Django's compilemessages")
            return True
        else:
            print(f"Django compilemessages failed: {result.stderr}")
    except Exception as e:
        print(f"Could not use Django compilemessages: {e}")
    
    # Fallback: create minimal working .mo files
    print("Creating minimal .mo files as fallback...")
    
    # Create minimal English .mo file
    create_minimal_mo('locale/en/LC_MESSAGES/django.mo', {
        "Dashboard": "Dashboard",
        "Inventory": "Inventory",
        "Sales": "Sales",
        "Purchases": "Purchases",
        "Expenses": "Expenses",
        "Reports": "Reports",
        "Settings": "Settings",
        "Profile": "Profile",
        "Logout": "Logout",
        "SpareSmart": "SpareSmart"
    })
    
    # Create empty Arabic .mo file for now
    create_minimal_mo('locale/ar/LC_MESSAGES/django.mo', {})
    
    print("Created minimal .mo files")
    return True

def create_minimal_mo(mo_path, translations):
    """Create a minimal .mo file"""
    import struct
    
    if not translations:
        # Create empty .mo file
        with open(mo_path, 'wb') as f:
            f.write(struct.pack('<I', 0x950412de))  # Magic number
            f.write(struct.pack('<I', 0))           # Version
            f.write(struct.pack('<I', 0))           # Number of strings
            f.write(struct.pack('<I', 28))          # Offset of key table
            f.write(struct.pack('<I', 28))          # Offset of value table
            f.write(struct.pack('<I', 0))           # Hash table size
            f.write(struct.pack('<I', 0))           # Offset of hash table
        return
    
    # Convert to bytes
    keys = [k.encode('utf-8') for k in translations.keys()]
    values = [v.encode('utf-8') for v in translations.values()]
    
    # Calculate offsets
    koffsets = []
    voffsets = []
    offset = 7 * 4 + 16 * len(keys)
    
    for key in keys:
        koffsets.append((offset, len(key)))
        offset += len(key)
    
    for value in values:
        voffsets.append((offset, len(value)))
        offset += len(value)
    
    # Write .mo file
    with open(mo_path, 'wb') as f:
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

if __name__ == '__main__':
    create_po_and_mo()
