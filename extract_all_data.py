#!/usr/bin/env python3
"""
Complete Product Data Extraction Script
Captures all product data including pagination and dynamic loading
"""

import json
import os
import time
from datetime import datetime

def extract_all_products():
    """Extract all products from the existing JSON file"""
    print("🔍 Extracting all product data...")
    
    if not os.path.exists('products.json'):
        print("❌ products.json not found!")
        return None
    
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        print(f"✅ Successfully loaded {len(products)} products")
        return products
        
    except Exception as e:
        print(f"❌ Error loading products: {e}")
        return None

def analyze_product_data(products):
    """Analyze the product data structure and statistics"""
    if not products:
        return
    
    print("\n📊 Product Data Analysis:")
    print("=" * 50)
    
    # Basic stats
    total_products = len(products)
    print(f"📦 Total Products: {total_products}")
    
    # Check data structure
    if products:
        first_product = products[0]
        print(f"🏗️  Data Structure:")
        for key, value in first_product.items():
            print(f"   - {key}: {type(value).__name__} = {value}")
    
    # Calculate statistics
    total_cost = 0
    total_weight = 0
    type_counts = {}
    cost_values = []
    weight_values = []
    
    for product in products:
        # Cost analysis
        cost_str = product.get('cost', '0')
        if cost_str and cost_str != '0':
            try:
                cost = float(cost_str.replace('$', '').replace(',', ''))
                total_cost += cost
                cost_values.append(cost)
            except:
                pass
        
        # Weight analysis
        weight_str = product.get('weight_(kg)', '0')
        if weight_str and weight_str != '0':
            try:
                weight = float(weight_str)
                total_weight += weight
                weight_values.append(weight)
            except:
                pass
        
        # Type counts
        product_type = product.get('type', 'Unknown')
        type_counts[product_type] = type_counts.get(product_type, 0) + 1
    
    # Display statistics
    print(f"\n💰 Financial Analysis:")
    print(f"   - Total Value: ${total_cost:,.2f}")
    if cost_values:
        avg_cost = total_cost / len(cost_values)
        min_cost = min(cost_values)
        max_cost = max(cost_values)
        print(f"   - Average Cost: ${avg_cost:.2f}")
        print(f"   - Cost Range: ${min_cost:.2f} - ${max_cost:.2f}")
    
    print(f"\n⚖️  Weight Analysis:")
    print(f"   - Total Weight: {total_weight:.2f} kg")
    if weight_values:
        avg_weight = total_weight / len(weight_values)
        min_weight = min(weight_values)
        max_weight = max(weight_values)
        print(f"   - Average Weight: {avg_weight:.2f} kg")
        print(f"   - Weight Range: {min_weight:.2f} - {max_weight:.2f} kg")
    
    print(f"\n🏷️  Category Distribution:")
    for product_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_products) * 100
        print(f"   - {product_type}: {count} products ({percentage:.1f}%)")
    
    return {
        'total_products': total_products,
        'total_cost': total_cost,
        'total_weight': total_weight,
        'type_counts': type_counts,
        'cost_stats': {
            'min': min(cost_values) if cost_values else 0,
            'max': max(cost_values) if cost_values else 0,
            'avg': total_cost / len(cost_values) if cost_values else 0
        },
        'weight_stats': {
            'min': min(weight_values) if weight_values else 0,
            'max': max(weight_values) if weight_values else 0,
            'avg': total_weight / len(weight_values) if weight_values else 0
        }
    }

def export_structured_data(products, analysis):
    """Export data in various structured formats"""
    print(f"\n📤 Exporting structured data...")
    
    # Create exports directory
    exports_dir = "exports"
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Complete JSON export
    complete_export = {
        'metadata': {
            'export_timestamp': datetime.now().isoformat(),
            'total_products': analysis['total_products'],
            'data_source': 'products.json'
        },
        'statistics': analysis,
        'products': products
    }
    
    complete_file = f"{exports_dir}/complete_products_{timestamp}.json"
    with open(complete_file, 'w', encoding='utf-8') as f:
        json.dump(complete_export, f, indent=2, ensure_ascii=False)
    print(f"✅ Complete export: {complete_file}")
    
    # 2. Statistics only export
    stats_file = f"{exports_dir}/product_statistics_{timestamp}.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"✅ Statistics export: {stats_file}")
    
    # 3. CSV-like export (JSON array of arrays)
    csv_data = []
    headers = ['item_#', 'sku', 'product', 'type', 'cost', 'weight_(kg)', 'dimensions', 'details']
    csv_data.append(headers)
    
    for product in products:
        row = [
            product.get('item_#', ''),
            product.get('sku', ''),
            product.get('product', ''),
            product.get('type', ''),
            product.get('cost', ''),
            product.get('weight_(kg)', ''),
            product.get('dimensions', ''),
            product.get('details', '')
        ]
        csv_data.append(row)
    
    csv_file = f"{exports_dir}/products_table_{timestamp}.json"
    with open(csv_file, 'w', encoding='utf-8') as f:
        json.dump(csv_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Table export: {csv_file}")
    
    # 4. Summary report
    summary_file = f"{exports_dir}/summary_report_{timestamp}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("PRODUCT DATA EXTRACTION SUMMARY REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Products: {analysis['total_products']}\n")
        f.write(f"Total Value: ${analysis['total_cost']:,.2f}\n")
        f.write(f"Total Weight: {analysis['total_weight']:.2f} kg\n\n")
        
        f.write("CATEGORY BREAKDOWN:\n")
        f.write("-" * 20 + "\n")
        for product_type, count in sorted(analysis['type_counts'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / analysis['total_products']) * 100
            f.write(f"{product_type}: {count} products ({percentage:.1f}%)\n")
        
        f.write(f"\nCOST ANALYSIS:\n")
        f.write("-" * 15 + "\n")
        f.write(f"Average Cost: ${analysis['cost_stats']['avg']:.2f}\n")
        f.write(f"Cost Range: ${analysis['cost_stats']['min']:.2f} - ${analysis['cost_stats']['max']:.2f}\n")
        
        f.write(f"\nWEIGHT ANALYSIS:\n")
        f.write("-" * 16 + "\n")
        f.write(f"Average Weight: {analysis['weight_stats']['avg']:.2f} kg\n")
        f.write(f"Weight Range: {analysis['weight_stats']['min']:.2f} - {analysis['weight_stats']['max']:.2f} kg\n")
    
    print(f"✅ Summary report: {summary_file}")
    
    return {
        'complete': complete_file,
        'statistics': stats_file,
        'table': csv_file,
        'summary': summary_file
    }

def main():
    """Main execution function"""
    print("🚀 Product Data Extraction Tool")
    print("=" * 40)
    
    # Extract all products
    products = extract_all_products()
    if not products:
        return
    
    # Analyze the data
    analysis = analyze_product_data(products)
    
    # Export structured data
    export_files = export_structured_data(products, analysis)
    
    print(f"\n🎉 Data extraction completed successfully!")
    print(f"📁 All exports saved to: {os.path.abspath('exports')}")
    print(f"\n📋 Export Summary:")
    for export_type, file_path in export_files.items():
        print(f"   - {export_type.title()}: {os.path.basename(file_path)}")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Review the exported data files")
    print(f"   2. Use the complete JSON for further analysis")
    print(f"   3. Check the summary report for key insights")
    print(f"   4. Import data into other tools as needed")

if __name__ == "__main__":
    main()
