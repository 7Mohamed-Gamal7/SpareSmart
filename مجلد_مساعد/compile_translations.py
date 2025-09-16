#!/usr/bin/env python
"""
Manual script to compile .po files to .mo files
"""
import os
import struct
import array
from django.conf import settings
from django.core.management import execute_from_command_line

def compile_po_files():
    """Use Django's compilemessages command"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
        execute_from_command_line(['manage.py', 'compilemessages'])
        print("Successfully compiled translation files")
    except Exception as e:
        print(f"Error compiling translations: {e}")
        # Fallback: create empty .mo files
        create_empty_mo_files()

def create_empty_mo_files():
    """Create minimal .mo files manually"""
    locale_dir = 'locale'
    
    for root, dirs, files in os.walk(locale_dir):
        for file in files:
            if file.endswith('.po'):
                mo_file = os.path.join(root, file.replace('.po', '.mo'))
                print(f"Creating minimal .mo file: {mo_file}")
                
                # Create a minimal valid .mo file
                with open(mo_file, 'wb') as f:
                    # Magic number for .mo files
                    f.write(struct.pack('<I', 0x950412de))
                    # Version
                    f.write(struct.pack('<I', 0))
                    # Number of strings
                    f.write(struct.pack('<I', 0))
                    # Offset of table with original strings
                    f.write(struct.pack('<I', 28))
                    # Offset of table with translation strings
                    f.write(struct.pack('<I', 28))
                    # Hash table size
                    f.write(struct.pack('<I', 0))
                    # Offset of hash table
                    f.write(struct.pack('<I', 28))

if __name__ == '__main__':
    compile_po_files()