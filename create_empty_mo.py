#!/usr/bin/env python3
"""
Create an empty .mo file for Arabic to prevent loading errors
"""
import struct
import os

def create_empty_mo_file(mo_path):
    """Create an empty .mo file"""
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    
    # Write minimal .mo file with no translations
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

def main():
    print("Creating empty Arabic .mo file...")
    
    # Create empty Arabic .mo file
    ar_mo_path = 'locale/ar/LC_MESSAGES/django.mo'
    create_empty_mo_file(ar_mo_path)
    print(f"Created empty {ar_mo_path}")
    
    print("Done!")

if __name__ == '__main__':
    main()
