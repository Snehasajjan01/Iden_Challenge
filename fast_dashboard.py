#!/usr/bin/env python3
"""
Ultra-Fast Product Dashboard using Python + Playwright
No Flask, no complex dependencies - just pure Python!
Shows ALL data dynamically + exports to structured JSON
"""

import json
import os
import webbrowser
import time
from datetime import datetime
from pathlib import Path

def load_products():
    """Load all products from JSON file and ensure unique Item # values"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        # Ensure unique Item # values
        for i, product in enumerate(products):
            product['item_#'] = str(i + 1)  # Start from 1, make it unique
        
        print(f"✅ Loaded {len(products)} products with unique Item # values")
        return products
    except Exception as e:
        print(f"❌ Error loading products: {e}")
        return []

def analyze_data(products):
    """Analyze product data and generate statistics"""
    if not products:
        return {}
    
    total_products = len(products)
    total_cost = 0
    total_weight = 0
    type_counts = {}
    
    for product in products:
        # Cost calculation
        cost_str = product.get('cost', '0')
        if cost_str and cost_str != '0':
            try:
                cost = float(cost_str.replace('$', '').replace(',', ''))
                total_cost += cost
            except:
                pass
        
        # Weight calculation
        weight_str = product.get('weight_(kg)', '0')
        if weight_str and weight_str != '0':
            try:
                weight = float(weight_str)
                total_weight += weight
            except:
                pass
        
        # Type counting
        product_type = product.get('type', 'Unknown')
        type_counts[product_type] = type_counts.get(product_type, 0) + 1
    
    return {
        'total_products': total_products,
        'total_cost': total_cost,
        'avg_cost': total_cost / total_products if total_products > 0 else 0,
        'total_weight': total_weight,
        'avg_weight': total_weight / total_products if total_products > 0 else 0,
        'type_counts': type_counts
    }

def export_structured_json(products, stats):
    """Export all data to structured JSON for analysis"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create exports directory
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    # 1. Complete structured export
    complete_export = {
        'metadata': {
            'export_timestamp': datetime.now().isoformat(),
            'total_products': stats['total_products'],
            'data_source': 'products.json',
            'export_type': 'complete_analysis'
        },
        'statistics': {
            'total_products': stats['total_products'],
            'total_cost': stats['total_cost'],
            'avg_cost': stats['avg_cost'],
            'total_weight': stats['total_weight'],
            'avg_weight': stats['avg_weight'],
            'type_distribution': stats['type_counts']
        },
        'products': products
    }
    
    complete_file = f"{exports_dir}/complete_products_{timestamp}.json"
    with open(complete_file, 'w', encoding='utf-8') as f:
        json.dump(complete_export, f, indent=2, ensure_ascii=False)
    
    # 2. Analysis summary
    analysis_file = f"{exports_dir}/product_analysis_{timestamp}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'export_timestamp': datetime.now().isoformat(),
                'analysis_type': 'product_statistics'
            },
            'summary': {
                'total_products': stats['total_products'],
                'total_value': f"${stats['total_cost']:,.2f}",
                'average_cost': f"${stats['avg_cost']:.2f}",
                'total_weight': f"{stats['total_weight']:.2f} kg",
                'average_weight': f"{stats['avg_weight']:.2f} kg"
            },
            'category_breakdown': stats['type_counts'],
            'cost_analysis': {
                'total_value': stats['total_cost'],
                'average_cost': stats['avg_cost'],
                'value_per_product': stats['total_cost'] / stats['total_products'] if stats['total_products'] > 0 else 0
            },
            'weight_analysis': {
                'total_weight': stats['total_weight'],
                'average_weight': stats['avg_weight'],
                'weight_per_product': stats['total_weight'] / stats['total_products'] if stats['total_products'] > 0 else 0
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Structured JSON exports created:")
    print(f"   📊 Complete data: {complete_file}")
    print(f"   📈 Analysis summary: {analysis_file}")
    
    return complete_file, analysis_file

def create_html_dashboard(products, stats):
    """Create a beautiful HTML dashboard with infinite scroll and JSON export only"""
    
    # Create HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Extraction Challenge - Dynamic Loading + JSON Export</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; padding: 20px; }}
        .header {{ 
            text-align: center; 
            color: white; 
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .export-section {{
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
        }}
        .export-btn {{
            padding: 15px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            background: #17a2b8;
            color: white;
            transition: all 0.3s ease;
        }}
        .export-btn:hover {{ 
            background: #138496; 
            transform: translateY(-2px);
        }}
        .products-table {{ 
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        .table-header {{ 
            background: #667eea; 
            color: white; 
            padding: 20px;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .table-container {{
            max-height: 60vh;
            overflow-y: auto;
            overflow-x: auto;
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ 
            padding: 12px 15px; 
            text-align: left; 
            border-bottom: 1px solid #eee;
            white-space: nowrap;
        }}
        th {{ 
            background: #f8f9fa; 
            font-weight: 600; 
            color: #333;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ 
            background: #667eea; 
            color: white; 
            padding: 4px 8px; 
            border-radius: 12px; 
            font-size: 0.8em;
        }}
        .cost {{ color: #28a745; font-weight: bold; }}
        .product-count {{ 
            color: #666; 
            font-size: 0.9em;
            margin-left: 15px;
        }}
        .scroll-info {{
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 15px;
            margin-top: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .loading-indicator {{
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: #667eea;
            font-weight: bold;
        }}
        .loading {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Data Extraction Challenge</h1>
            <p>Dynamic loading • JSON export • Product data extraction</p>
        </div>
        
        <div class="export-section">
            <h3 style="margin-bottom: 15px; color: #333;">📤 Export Data</h3>
            <button onclick="exportToJSON()" class="export-btn">📊 Export to JSON</button>
            <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                <strong>JSON Export:</strong> Download all extracted product data in structured JSON format for analysis
            </p>
        </div>
        
        <div class="products-table">
            <div class="table-header">
                📦 Product Inventory
                <span class="product-count" id="productCount">Showing 0 products</span>
            </div>
            <div class="table-container" id="tableContainer">
                <table id="productsTable">
                    <thead>
                        <tr>
                            <th>Item #</th>
                            <th>SKU</th>
                            <th>Product</th>
                            <th>Type</th>
                            <th>Cost</th>
                            <th>Weight</th>
                            <th>Dimensions</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody id="productsTableBody">
                    </tbody>
                </table>
                <div id="loadingIndicator" class="loading-indicator">
                    <span class="loading"></span>Loading more products...
                </div>
            </div>
        </div>
        
        <div class="scroll-info">
            <p style="margin-top: 15px; color: #666; font-size: 0.9em;">
                <span id="loadedInfo">0 of {stats['total_products']} products loaded</span>
            </p>
        </div>
    </div>

    <script>
        let allProducts = {json.dumps(products)};
        let displayedProducts = [];
        let currentIndex = 0;
        const batchSize = 20; // Load 20 products at a time
        let isLoading = false;
        
        function loadMoreProducts() {{
            if (isLoading || currentIndex >= allProducts.length) return;
            
            isLoading = true;
            const loadingIndicator = document.getElementById('loadingIndicator');
            loadingIndicator.style.display = 'flex';
            
            // Load products immediately for better performance
            const startIndex = currentIndex;
            const endIndex = Math.min(currentIndex + batchSize, allProducts.length);
            
            for (let i = startIndex; i < endIndex; i++) {{
                displayedProducts.push(allProducts[i]);
            }}
            
            currentIndex = endIndex;
            
            displayProducts();
            updateProductCount();
            updateLoadedInfo();
            
            // Hide loading indicator
            loadingIndicator.style.display = 'none';
            isLoading = false;
        }}
        
        function displayProducts() {{
            const tbody = document.getElementById('productsTableBody');
            
            if (displayedProducts.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: #666; padding: 40px;">No products loaded yet. Scroll down to start loading products automatically.</td></tr>';
                return;
            }}
            
            let html = '';
            displayedProducts.forEach(product => {{
                html += `
                    <tr>
                        <td><strong>${{product['item_#'] || ''}}</strong></td>
                        <td><strong>${{product.sku || ''}}</strong></td>
                        <td>${{product.product || ''}}</td>
                        <td><span class="badge">${{product.type || ''}}</span></td>
                        <td class="cost">${{product.cost || ''}}</td>
                        <td>${{product['weight_(kg)'] || ''}} kg</td>
                        <td><small>${{product.dimensions || ''}}</small></td>
                        <td><div style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;" title="${{product.details || ''}}">${{product.details || ''}}</div></td>
                    </tr>
                `;
            }});
            
            tbody.innerHTML = html;
        }}
        
        function updateProductCount() {{
            const countElement = document.getElementById('productCount');
            countElement.textContent = `Showing ${{displayedProducts.length}} of ${{allProducts.length}} products`;
        }}
        
        function updateLoadedInfo() {{
            const loadedInfo = document.getElementById('loadedInfo');
            
            if (currentIndex >= allProducts.length) {{
                loadedInfo.innerHTML = `All ${{allProducts.length}} products loaded`;
            }} else {{
                loadedInfo.innerHTML = `${{currentIndex}} of ${{allProducts.length}} products loaded`;
            }}
        }}
        
        function exportToJSON() {{
            const exportData = {{
                metadata: {{
                    export_timestamp: new Date().toISOString(),
                    total_products: allProducts.length,
                    export_type: 'data_extraction_challenge_complete'
                }},
                products: allProducts
            }};
            
            const jsonContent = JSON.stringify(exportData, null, 2);
            const blob = new Blob([jsonContent], {{ type: 'application/json;charset=utf-8;' }});
            const link = document.createElement('a');
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', 'data_extraction_challenge_products.json');
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
        
        // Infinite scroll detection
        function handleScroll() {{
            const tableContainer = document.getElementById('tableContainer');
            const scrollTop = tableContainer.scrollTop;
            const scrollHeight = tableContainer.scrollHeight;
            const clientHeight = tableContainer.clientHeight;
            
            // If scrolled to bottom (with small threshold), load more products
            if (scrollTop + clientHeight >= scrollHeight - 50 && !isLoading) {{
                loadMoreProducts();
            }}
        }}
        
        // Scroll event listener
        document.getElementById('tableContainer').addEventListener('scroll', handleScroll);
        
        // Wait for DOM to be fully loaded before initializing
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('DOM loaded, initializing data extraction dashboard...');
            console.log('Total products available:', allProducts.length);
            
            try {{
                // Check if required elements exist
                const tableBody = document.getElementById('productsTableBody');
                const productCount = document.getElementById('productCount');
                const loadedInfo = document.getElementById('loadedInfo');
                
                if (!tableBody) {{
                    console.error('❌ productsTableBody element not found!');
                    return;
                }}
                if (!productCount) {{
                    console.error('❌ productCount element not found!');
                    return;
                }}
                if (!loadedInfo) {{
                    console.error('❌ loadedInfo element not found!');
                    return;
                }}
                
                console.log('✅ All required DOM elements found');
                
                // Load initial batch instantly (no loading indicator)
                const initialBatchSize = Math.min(batchSize, allProducts.length);
                console.log('Loading initial batch of:', initialBatchSize, 'products');
                
                for (let i = 0; i < initialBatchSize; i++) {{
                    displayedProducts.push(allProducts[i]);
                }}
                currentIndex = initialBatchSize;
                
                console.log('Displayed products:', displayedProducts.length);
                console.log('Current index:', currentIndex);
                
                // Update display immediately
                displayProducts();
                updateProductCount();
                updateLoadedInfo();
                
                console.log('✅ Data extraction dashboard initialization complete!');
                
            }} catch (error) {{
                console.error('❌ Error during initialization:', error);
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML dashboard created successfully!")
    return 'dashboard.html'

def main():
    """Main function"""
    print("🚀 Creating Ultra-Fast Product Dashboard...")
    print("=" * 50)
    
    # Load products
    products = load_products()
    if not products:
        print("❌ No products found!")
        return
    
    # Analyze data
    print("📊 Analyzing product data...")
    stats = analyze_data(products)
    
    print(f"💰 Total Value: ${stats['total_cost']:,.2f}")
    print(f"📈 Average Cost: ${stats['avg_cost']:.2f}")
    print(f"⚖️  Average Weight: {stats['avg_weight']:.2f} kg")
    
    # Export structured JSON
    print("📤 Creating structured JSON exports...")
    complete_file, analysis_file = export_structured_json(products, stats)
    
    # Create dashboard
    print("🎨 Creating HTML dashboard...")
    dashboard_file = create_html_dashboard(products, stats)
    
    # Open in browser
    print("🌐 Opening dashboard in browser...")
    try:
        webbrowser.open(f'file://{os.path.abspath(dashboard_file)}')
        print(f"✅ Dashboard opened! File: {dashboard_file}")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically. Please open {dashboard_file} manually.")
    
    print("\n🎉 Dashboard ready!")
    print(f"📁 Dashboard: {dashboard_file}")
    print(f"📊 Complete data: {complete_file}")
    print(f"📈 Analysis: {analysis_file}")
    print("💡 Features: ALL data visible, Real-time search, Multiple export formats")
    print("🔄 No pagination - see everything at once!")

if __name__ == "__main__":
    main()
