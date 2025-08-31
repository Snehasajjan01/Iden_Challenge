#!/usr/bin/env python3
"""
Simple Flask application for Product Dashboard
"""

import json
import os
from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# Configuration
PRODUCTS_FILE = "products.json"

def load_products():
    """Load products from JSON file"""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading products: {e}")
            return []
    return []

def get_stats(products):
    """Calculate statistics from products data"""
    if not products:
        return {}
    
    total_products = len(products)
    total_cost = sum(float(p.get('cost', '0').replace('$', '').replace(',', '')) for p in products if p.get('cost'))
    avg_cost = total_cost / total_products if total_products > 0 else 0
    
    # Count by type
    type_counts = {}
    for product in products:
        product_type = product.get('type', 'Unknown')
        type_counts[product_type] = type_counts.get(product_type, 0) + 1
    
    # Weight statistics
    weights = [float(p.get('weight_(kg)', '0')) for p in products if p.get('weight_(kg)')]
    avg_weight = sum(weights) / len(weights) if weights else 0
    
    return {
        'total_products': total_products,
        'total_cost': f"${total_cost:,.2f}",
        'avg_cost': f"${avg_cost:.2f}",
        'avg_weight': f"{avg_weight:.2f} kg",
        'type_counts': type_counts
    }

@app.route('/')
def index():
    """Main page with dashboard"""
    products = load_products()
    stats = get_stats(products)
    return render_template('index.html', stats=stats, total_products=len(products))

@app.route('/products')
def products():
    """Products listing page"""
    products = load_products()
    return render_template('products.html', products=products)

@app.route('/api/search')
def search_products():
    """API endpoint for searching products"""
    query = request.args.get('q', '').lower()
    products = load_products()
    
    if not query:
        return jsonify(products[:50])  # Return first 50 if no search query
    
    filtered_products = []
    for product in products:
        if (query in product.get('sku', '').lower() or
            query in product.get('product', '').lower() or
            query in product.get('type', '').lower() or
            query in product.get('details', '').lower()):
            filtered_products.append(product)
    
    return jsonify(filtered_products[:100])  # Limit results

@app.route('/api/stats')
def get_stats_api():
    """API endpoint for statistics"""
    products = load_products()
    return jsonify(get_stats(products))

@app.route('/api/products')
def get_products_api():
    """API endpoint for all products"""
    products = load_products()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return jsonify({
        'products': products[start_idx:end_idx],
        'total': len(products),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(products) + per_page - 1) // per_page
    })

@app.route('/export/all')
def export_all_products():
    """Export all products to JSON"""
    products = load_products()
    return jsonify({
        'total_products': len(products),
        'products': products,
        'export_timestamp': str(datetime.datetime.now())
    })

if __name__ == '__main__':
    print("🚀 Starting Simple Product Dashboard...")
    print(f"📊 Loading products from: {PRODUCTS_FILE}")
    
    products = load_products()
    if products:
        print(f"✅ Loaded {len(products)} products")
        stats = get_stats(products)
        print(f"💰 Total value: {stats.get('total_cost', 'N/A')}")
        print(f"📈 Average cost: {stats.get('avg_cost', 'N/A')}")
    else:
        print("⚠️  No products found!")
    
    print("\n🌐 Starting Flask server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
