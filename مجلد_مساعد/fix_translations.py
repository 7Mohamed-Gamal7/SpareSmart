#!/usr/bin/env python3
"""
Simple script to create .mo files from .po files for Django translations
"""
import struct
import os
import re

def parse_po_file(po_content):
    """Parse a .po file and extract msgid/msgstr pairs"""
    translations = {}
    
    # Split into blocks
    blocks = re.split(r'\n\s*\n', po_content)
    
    for block in blocks:
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        msgid = None
        msgstr = None
        
        for line in lines:
            if line.startswith('msgid "') and line.endswith('"'):
                msgid = line[7:-1]  # Remove 'msgid "' and '"'
            elif line.startswith('msgstr "') and line.endswith('"'):
                msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
        
        if msgid and msgstr and msgid != "":  # Skip empty msgid (header)
            translations[msgid] = msgstr
    
    return translations

def create_mo_file(translations, mo_path):
    """Create a .mo file from translations dictionary"""

    # Ensure directory exists
    os.makedirs(os.path.dirname(mo_path), exist_ok=True)

    # Convert to bytes with proper encoding
    keys = []
    values = []

    for msgid, msgstr in translations.items():
        # Ensure strings are properly encoded as UTF-8
        try:
            key_bytes = msgid.encode('utf-8')
            value_bytes = msgstr.encode('utf-8')
            keys.append(key_bytes)
            values.append(value_bytes)
        except UnicodeEncodeError as e:
            print(f"Warning: Skipping translation due to encoding error: {msgid} -> {msgstr}")
            continue

    if not keys:
        print("Warning: No valid translations found")
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
    print("Creating .mo files from .po files...")
    
    # Process English
    en_po_path = 'locale/en/LC_MESSAGES/django.po'
    en_mo_path = 'locale/en/LC_MESSAGES/django.mo'
    
    if os.path.exists(en_po_path):
        print(f"Processing {en_po_path}...")
        with open(en_po_path, 'r', encoding='utf-8') as f:
            po_content = f.read()
        
        translations = parse_po_file(po_content)
        print(f"Found {len(translations)} English translations")
        
        create_mo_file(translations, en_mo_path)
        print(f"Created {en_mo_path}")
    else:
        print(f"Warning: {en_po_path} not found")
    
    # Process Arabic
    ar_po_path = 'locale/ar/LC_MESSAGES/django.po'
    ar_mo_path = 'locale/ar/LC_MESSAGES/django.mo'
    
    if os.path.exists(ar_po_path):
        print(f"Processing {ar_po_path}...")
        with open(ar_po_path, 'r', encoding='utf-8') as f:
            po_content = f.read()
        
        translations = parse_po_file(po_content)
        print(f"Found {len(translations)} Arabic translations")
        
        create_mo_file(translations, ar_mo_path)
        print(f"Created {ar_mo_path}")
    else:
        print(f"Warning: {ar_po_path} not found")
    
    print("Done!")

if __name__ == '__main__':
    main()
