import struct

# Create a minimal valid .mo file for English
def create_mo_file(po_content, mo_path):
    """Create a simple .mo file from .po content"""
    
    # Parse simple msgid/msgstr pairs
    strings = {}
    lines = po_content.split('\n')
    msgid = None
    msgstr = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip comments, empty lines, and metadata
        if not line or line.startswith('#') or line.startswith('"'):
            i += 1
            continue
            
        if line.startswith('msgid "') and line.endswith('"'):
            msgid = line[7:-1]  # Remove 'msgid "' and '"'
            # Skip empty msgid (header)
            if not msgid:
                # Skip until next msgid
                while i < len(lines) and not lines[i].strip().startswith('msgid '):
                    i += 1
                continue
                
        elif line.startswith('msgstr "') and line.endswith('"'):
            msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
            if msgid is not None and msgstr:
                # Use English text as both key and value for English locale
                strings[msgid.encode('utf-8')] = msgstr.encode('utf-8')
            msgid = None
            msgstr = None
            
        i += 1
    
    # If no translations found, create basic ones
    if not strings:
        basic_translations = {
            b'Dashboard': b'Dashboard',
            b'Inventory': b'Inventory', 
            b'Sales': b'Sales',
            b'Purchases': b'Purchases',
            b'Expenses': b'Expenses',
            b'Reports': b'Reports',
            b'Settings': b'Settings',
            b'Profile': b'Profile',
            b'Logout': b'Logout'
        }
        strings = basic_translations
    
    # Write .mo file
    with open(mo_path, 'wb') as f:
        # Magic number
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of strings  
        f.write(struct.pack('<I', len(strings)))
        
        # Calculate offsets
        koffsets = []
        voffsets = []
        kencoded = []
        vencoded = []
        
        offset = 7 * 4 + 16 * len(strings)
        
        for k, v in strings.items():
            kencoded.append(k)
            vencoded.append(v)
            koffsets.append((len(k), offset))
            offset += len(k)
            voffsets.append((len(v), offset))
            offset += len(v)
        
        # Offset of table with original strings
        f.write(struct.pack('<I', 7 * 4))
        # Offset of table with translation strings  
        f.write(struct.pack('<I', 7 * 4 + 8 * len(strings)))
        # Hash table size
        f.write(struct.pack('<I', 0))
        # Offset of hash table
        f.write(struct.pack('<I', 0))
        
        # Write string tables
        for o, l in koffsets:
            f.write(struct.pack('<II', l, o))
        for o, l in voffsets:
            f.write(struct.pack('<II', l, o))
            
        # Write strings
        for k in kencoded:
            f.write(k)
        for v in vencoded:
            f.write(v)

# Read English .po file and create .mo file
with open('locale/en/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
    po_content = f.read()

create_mo_file(po_content, 'locale/en/LC_MESSAGES/django.mo')
print("Created English .mo file")

# Check if Arabic .mo exists, if not create it
import os
if not os.path.exists('locale/ar/LC_MESSAGES/django.mo'):
    # Read Arabic .po file and create .mo file
    with open('locale/ar/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
        ar_po_content = f.read()
    
    create_mo_file(ar_po_content, 'locale/ar/LC_MESSAGES/django.mo')
    print("Created Arabic .mo file")
else:
    print("Arabic .mo file already exists")