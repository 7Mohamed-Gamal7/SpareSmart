#!/usr/bin/env python3
"""
Test the dashboard fix for materials column error
"""
import os
import django
import requests
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sparesmart.settings')
django.setup()

from inventory.models import Product, Category, Brand
from accounts.models import User

def test_database_schema():
    """Test that the materials column exists and works"""
    
    print("🔍 Testing Database Schema...")
    print("-" * 50)
    
    try:
        # Test that we can query products without error
        products_count = Product.objects.count()
        print(f"✅ Products table accessible: {products_count} products found")
        
        # Test that we can access the materials field
        if products_count > 0:
            product = Product.objects.first()
            materials = product.materials
            print(f"✅ Materials field accessible: '{materials}'")
        else:
            print("⚠️  No products in database to test materials field")
            
        return True
        
    except Exception as e:
        print(f"❌ Database schema error: {e}")
        return False

def test_dashboard_view():
    """Test the dashboard view that was causing the error"""
    
    print("\n🌐 Testing Dashboard View...")
    print("-" * 50)
    
    try:
        from dashboard.views import home
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        
        # Get a superuser for the request
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            request.user = superuser
            print(f"✅ Using superuser: {superuser.username}")
        else:
            print("⚠️  No superuser found, using anonymous user")
            request.user = AnonymousUser()
        
        # Test the view
        response = home(request)
        print(f"✅ Dashboard view executed successfully")
        print(f"✅ Response status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard view error: {e}")
        return False

def test_top_products_query():
    """Test the specific query that was failing"""
    
    print("\n📊 Testing Top Products Query...")
    print("-" * 50)
    
    try:
        from django.db.models import Sum
        
        # This is the exact query from the dashboard view
        top_products = Product.objects.annotate(
            total_sold=Sum('saleitem__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')[:5]
        
        print(f"✅ Top products query executed successfully")
        print(f"✅ Found {top_products.count()} top selling products")
        
        # Test accessing materials field for each product
        for i, product in enumerate(top_products, 1):
            materials = product.materials
            print(f"  {i}. {product.name} - Materials: '{materials}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Top products query error: {e}")
        return False

def test_dashboard_http():
    """Test the dashboard via HTTP request"""
    
    print("\n🌍 Testing Dashboard HTTP Access...")
    print("-" * 50)
    
    try:
        response = requests.get('http://127.0.0.1:8000/dashboard/', timeout=10)
        
        print(f"✅ HTTP Status: {response.status_code}")
        print(f"✅ Content Length: {len(response.text)} characters")
        print(f"✅ Content Type: {response.headers.get('content-type', 'N/A')}")
        
        # Check if the response contains expected content
        if 'Top Selling' in response.text or 'المنتجات' in response.text:
            print("✅ Dashboard contains expected top products section")
        else:
            print("⚠️  Top products section not found in response")
        
        # Check for error indicators
        if 'OperationalError' in response.text:
            print("❌ OperationalError still present in response")
            return False
        elif 'materials' in response.text.lower() and 'error' in response.text.lower():
            print("❌ Materials-related error found in response")
            return False
        else:
            print("✅ No database errors found in response")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server")
        print("   Make sure the server is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ HTTP test error: {e}")
        return False

def create_test_data():
    """Create some test data if needed"""
    
    print("\n📝 Creating Test Data...")
    print("-" * 50)
    
    try:
        # Create a category if none exists
        if not Category.objects.exists():
            category = Category.objects.create(
                name="Test Category",
                description="Test category for materials field testing"
            )
            print(f"✅ Created test category: {category.name}")
        else:
            category = Category.objects.first()
            print(f"✅ Using existing category: {category.name}")
        
        # Create a brand if none exists
        if not Brand.objects.exists():
            brand = Brand.objects.create(
                name="Test Brand",
                description="Test brand for materials field testing"
            )
            print(f"✅ Created test brand: {brand.name}")
        else:
            brand = Brand.objects.first()
            print(f"✅ Using existing brand: {brand.name}")
        
        # Create a test product if none exists
        if not Product.objects.exists():
            product = Product.objects.create(
                name="Test Product",
                description="Test product for materials field testing",
                sku="TEST-001",
                category=category,
                brand=brand,
                cost_price=10.00,
                selling_price=15.00,
                materials="Steel, Plastic"  # Test the materials field
            )
            print(f"✅ Created test product: {product.name}")
            print(f"✅ Materials field set to: '{product.materials}'")
        else:
            product = Product.objects.first()
            print(f"✅ Using existing product: {product.name}")
            print(f"✅ Materials field value: '{product.materials}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return False

def main():
    """Main test function"""
    
    print("🔧 Dashboard Materials Column Fix - Comprehensive Test")
    print("=" * 80)
    
    # Run all tests
    tests = [
        ("Database Schema", test_database_schema),
        ("Test Data Creation", create_test_data),
        ("Dashboard View", test_dashboard_view),
        ("Top Products Query", test_top_products_query),
        ("HTTP Access", test_dashboard_http),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 Test Results Summary:")
    print("-" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<25} | {status}")
        if result:
            passed += 1
    
    print("-" * 40)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The materials column error has been successfully fixed!")
        print("✅ Dashboard should now load without OperationalError!")
        print("✅ Top selling products section should work correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("❌ Additional investigation may be needed")
    
    return passed == total

if __name__ == '__main__':
    main()
