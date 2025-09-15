# Create minimal empty .mo files to prevent translation crashes

import struct
import os

def create_empty_mo_file(path):
    """Create an empty but valid .mo file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        # Magic number for little-endian .mo files
        f.write(struct.pack('<I', 0x950412de))
        # Version (0)
        f.write(struct.pack('<I', 0))
        # Number of strings (0)
        f.write(struct.pack('<I', 0))
        # Offset of original strings table
        f.write(struct.pack('<I', 28))
        # Offset of translated strings table  
        f.write(struct.pack('<I', 28))
        # Size of hash table (0)
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 28))

# Create empty .mo files for both languages
create_empty_mo_file('locale/ar/LC_MESSAGES/django.mo')
create_empty_mo_file('locale/en/LC_MESSAGES/django.mo')

print("Created minimal .mo files to prevent translation errors")