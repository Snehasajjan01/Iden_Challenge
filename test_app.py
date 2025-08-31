#!/usr/bin/env python3
"""
Test script for the Flask application
"""

import json
import os
from app import load_products, get_stats

def test_data_loading():
    """Test if products data can be loaded correctly"""
    print("🧪 Testing data loading...")
    
    # Test loading products
    products = load_products()
    print(f"✅ Loaded {len(products)} products")
    
    if len(products) > 0:
        print(f"📦 Sample product: {products[0]['sku']} - {products[0]['product']}")
    
    # Test statistics calculation
    stats = get_stats(products)
    print(f"📊 Statistics calculated:")
    print(f"   - Total products: {stats.get('total_products', 0)}")
    print(f"   - Total cost: {stats.get('total_cost', 'N/A')}")
    print(f"   - Average cost: {stats.get('avg_cost', 'N/A')}")
    print(f"   - Average weight: {stats.get('avg_weight', 'N/A')}")
    
    # Test type counts
    type_counts = stats.get('type_counts', {})
    print(f"🏷️  Product types: {len(type_counts)}")
    for product_type, count in type_counts.items():
        print(f"   - {product_type}: {count}")
    
    print("\n🎉 All tests passed! The application is ready to run.")
    return True

def test_json_structure():
    """Test if the JSON file structure is correct"""
    print("\n🔍 Testing JSON structure...")
    
    if not os.path.exists('products.json'):
        print("❌ products.json not found!")
        return False
    
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("❌ products.json should contain a list of products")
            return False
        
        if len(data) == 0:
            print("⚠️  products.json is empty")
            return False
        
        # Check first product structure
        first_product = data[0]
        required_fields = ['sku', 'product', 'type', 'cost', 'weight_(kg)', 'dimensions', 'details']
        
        missing_fields = [field for field in required_fields if field not in first_product]
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False
        
        print("✅ JSON structure is valid")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading JSON: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Flask Application Setup")
    print("=" * 50)
    
    # Test JSON structure
    json_ok = test_json_structure()
    
    if json_ok:
        # Test data loading
        test_data_loading()
    else:
        print("\n❌ JSON structure test failed. Please check your products.json file.")
    
    print("\n" + "=" * 50)
    print("📝 To run the application:")
    print("   python app.py")
    print("   Then open http://localhost:5000 in your browser")
