#!/usr/bin/env python3
"""
Fix the materials column name mismatch
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from django.db import connection

def fix_materials_column():
    """Fix the materials column name"""
    
    print("🔧 Fixing materials column name...")
    print("-" * 50)
    
    cursor = connection.cursor()
    
    try:
        # Check if 'material' column exists
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        
        material_exists = False
        materials_exists = False
        
        for col in columns:
            col_name = col[1]
            if col_name == 'material':
                material_exists = True
            elif col_name == 'materials':
                materials_exists = True
        
        print(f"📊 Column status:")
        print(f"  'material' column exists: {material_exists}")
        print(f"  'materials' column exists: {materials_exists}")
        
        if material_exists and not materials_exists:
            print("\n🔄 Renaming 'material' column to 'materials'...")
            
            # SQLite doesn't support RENAME COLUMN directly in older versions
            # We need to use ALTER TABLE ... RENAME COLUMN (SQLite 3.25.0+)
            try:
                cursor.execute("ALTER TABLE products RENAME COLUMN material TO materials")
                print("✅ Successfully renamed column using ALTER TABLE RENAME COLUMN")
            except Exception as e:
                print(f"⚠️  ALTER TABLE RENAME COLUMN failed: {e}")
                print("🔄 Using alternative method...")
                
                # Alternative method: Create new table, copy data, rename
                # This is more complex but works with older SQLite versions
                # For now, let's try a simpler approach
                print("❌ Column rename failed. Will create a Django migration instead.")
                return False
                
        elif materials_exists:
            print("✅ 'materials' column already exists - no fix needed")
            return True
        else:
            print("❌ Neither 'material' nor 'materials' column found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing column: {e}")
        return False
    finally:
        cursor.close()

def create_migration_file():
    """Create a Django migration to fix the column name"""
    
    print("\n📝 Creating Django migration...")
    print("-" * 50)
    
    migration_content = '''# Generated migration to fix materials column name
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE products RENAME COLUMN material TO materials;",
            reverse_sql="ALTER TABLE products RENAME COLUMN materials TO material;",
        ),
    ]
'''
    
    # Write migration file
    migration_file = 'inventory/migrations/0003_fix_materials_column.py'
    
    try:
        with open(migration_file, 'w', encoding='utf-8') as f:
            f.write(migration_content)
        
        print(f"✅ Created migration file: {migration_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating migration file: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 Fix Materials Column Name Mismatch")
    print("=" * 60)
    
    # Try direct fix first
    success = fix_materials_column()
    
    if not success:
        # Create migration file
        migration_created = create_migration_file()
        
        if migration_created:
            print("\n" + "=" * 60)
            print("📋 Next Steps:")
            print("1. Run: python manage.py migrate")
            print("2. Test the dashboard page")
            print("3. Verify that the materials field works correctly")
        else:
            print("\n❌ Failed to create migration. Manual intervention required.")
    else:
        print("\n✅ Column fix completed successfully!")

if __name__ == '__main__':
    main()
