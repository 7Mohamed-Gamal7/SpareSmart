#!/usr/bin/env python3
"""
Check database schema for products table
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from django.db import connection

def check_products_table():
    """Check the products table schema"""
    
    print("🔍 Checking products table schema...")
    print("-" * 50)
    
    cursor = connection.cursor()
    
    try:
        # Get table info for products table
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        
        print(f"📊 Found {len(columns)} columns in products table:")
        print()
        
        materials_found = False
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, primary_key = col
            print(f"  {col_name:<20} | {col_type:<15} | {'NOT NULL' if not_null else 'NULL':<8} | {'PK' if primary_key else ''}")
            
            if col_name == 'materials':
                materials_found = True
        
        print()
        print("-" * 50)
        
        if materials_found:
            print("✅ 'materials' column EXISTS in the database")
        else:
            print("❌ 'materials' column MISSING from the database")
            
        return materials_found
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False
    finally:
        cursor.close()

def test_products_query():
    """Test querying products with materials field"""
    
    print("\n🧪 Testing products query...")
    print("-" * 50)
    
    try:
        from inventory.models import Product
        
        # Try to query products with materials field
        products = Product.objects.all()[:1]
        
        if products.exists():
            product = products.first()
            print(f"✅ Successfully queried product: {product.name}")
            
            # Try to access materials field
            try:
                materials = product.materials
                print(f"✅ Materials field accessible: '{materials}'")
                return True
            except Exception as e:
                print(f"❌ Error accessing materials field: {e}")
                return False
        else:
            print("⚠️  No products found in database")
            return True  # No error, just no data
            
    except Exception as e:
        print(f"❌ Error querying products: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 Database Schema Check - Products Table")
    print("=" * 60)
    
    # Check database schema
    schema_ok = check_products_table()
    
    # Test query
    query_ok = test_products_query()
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    
    if schema_ok and query_ok:
        print("✅ Database schema is correct")
        print("✅ Products table has 'materials' column")
        print("✅ No migration needed")
    elif not schema_ok:
        print("❌ 'materials' column missing from database")
        print("🔧 Need to create migration to add missing column")
    else:
        print("❌ Query issues detected")
        print("🔧 Need to investigate further")

if __name__ == '__main__':
    main()
