#!/usr/bin/env python3
"""
Create Arabic .mo file with proper encoding
"""
import struct
import os

def create_mo_file_safe(translations, mo_path):
    """Create a .mo file with safe encoding handling"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # Convert to bytes with safe encoding
    keys = []
    values = []
    
    for msgid, msgstr in translations.items():
        try:
            # Encode as UTF-8 and ensure it's valid
            key_bytes = msgid.encode('utf-8')
            value_bytes = msgstr.encode('utf-8')
            
            # Test decoding to ensure it's valid
            key_bytes.decode('utf-8')
            value_bytes.decode('utf-8')
            
            keys.append(key_bytes)
            values.append(value_bytes)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            print(f"Skipping invalid translation: {msgid} -> {msgstr} ({e})")
            continue
    
    if not keys:
        print("No valid translations found, creating empty file")
        # Create empty .mo file
        with open(mo_path, 'wb') as f:
            # Magic number (little endian)
            f.write(struct.pack('<I', 0x950412de))
            # Version
            f.write(struct.pack('<I', 0))
            # Number of strings (0)
            f.write(struct.pack('<I', 0))
            # Offset of key table
            f.write(struct.pack('<I', 7 * 4))
            # Offset of value table
            f.write(struct.pack('<I', 7 * 4))
            # Hash table size (0 = no hash table)
            f.write(struct.pack('<I', 0))
            # Offset of hash table
            f.write(struct.pack('<I', 0))
        return
    
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
    print("Creating Arabic .mo file with safe encoding...")
    
    # Basic Arabic translations (using simple ASCII-safe Arabic)
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
        "SpareSmart": "سبير سمارت"
    }
    
    # Create Arabic .mo file
    ar_mo_path = 'locale/ar/LC_MESSAGES/django.mo'
    create_mo_file_safe(ar_translations, ar_mo_path)
    print(f"Created {ar_mo_path}")
    
    print("Done!")

if __name__ == '__main__':
    main()
