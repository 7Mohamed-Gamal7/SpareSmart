#!/usr/bin/env python3
"""
اختبار الوصول للصفحات كمستخدم superuser
"""
import requests
import sys

def test_page_access():
    """اختبار الوصول للصفحات"""
    
    base_url = 'http://127.0.0.1:8000'
    
    # قائمة الصفحات للاختبار
    pages = [
        '/dashboard/',
        '/inventory/products/',
        '/sales/',
        '/purchases/',
        '/expenses/',
        '/reports/',
    ]
    
    print("🔍 اختبار الوصول للصفحات...")
    
    session = requests.Session()
    
    for page in pages:
        try:
            response = session.get(f"{base_url}{page}")
            status = "✅" if response.status_code == 200 else "❌"
            print(f"   {status} {page}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {page}: خطأ - {e}")

if __name__ == '__main__':
    test_page_access()
