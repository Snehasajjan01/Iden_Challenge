# Product Dashboard UI

A modern, responsive web interface for viewing and analyzing scraped product data from the Iden challenge project.

## Features

- **Dashboard Overview**: Statistics cards showing total products, total value, average cost, and average weight
- **Interactive Charts**: Bar chart and pie chart showing product distribution by category
- **Product Management**: Complete product listing with search, filtering, and sorting capabilities
- **Responsive Design**: Modern UI that works on desktop and mobile devices
- **Data Export**: Export filtered data to CSV format
- **Real-time Search**: Search products by SKU, name, type, or description
- **Pagination**: Efficient pagination for large datasets

## Screenshots

The UI includes:
- Beautiful gradient background with glass-morphism design
- Interactive statistics cards with hover effects
- Responsive charts using Chart.js
- Modern table design with hover effects
- Search and filter functionality
- Product detail modals

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure you have the data files**:
   - `products.json` - Your scraped product data
   - `session.json` - Browser session data (optional)

## Usage

1. **Start the Flask application**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Navigate between pages**:
   - **Dashboard** (`/`): Overview with statistics and charts
   - **Products** (`/products`): Complete product listing with search and filters

## API Endpoints

The application provides several API endpoints:

- `GET /api/products` - Get all products with pagination
- `GET /api/search?q=<query>` - Search products
- `GET /api/stats` - Get statistics

## Features in Detail

### Dashboard
- **Statistics Cards**: Total products, total value, average cost, average weight
- **Category Chart**: Bar chart showing product count by category
- **Distribution Chart**: Pie chart showing category distribution
- **Quick Actions**: Buttons for common tasks

### Products Page
- **Search**: Search by SKU, product name, type, or description
- **Filtering**: Filter by product type
- **Sorting**: Sort by SKU, name, cost, weight, or type
- **Pagination**: Navigate through large datasets
- **Export**: Download filtered data as CSV
- **Product Details**: Click the eye icon to view detailed product information

### Search Functionality
- **Real-time Search**: Search as you type
- **Modal Interface**: Clean search interface with results
- **Multiple Fields**: Search across SKU, name, type, and description

## Customization

### Styling
The UI uses CSS custom properties for easy theming:
- Primary colors: `--primary-color`, `--secondary-color`
- Success/Warning/Danger colors
- Glass-morphism effects with backdrop-filter

### Adding New Features
- **New Charts**: Add Chart.js configurations in the dashboard
- **Additional Filters**: Extend the filtering system in products.html
- **New Export Formats**: Add export functions for different file types

## Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Flask (Python)
- **Charts**: Chart.js
- **Styling**: Bootstrap 5 + Custom CSS
- **Icons**: Font Awesome 6
- **Responsive**: Mobile-first design approach

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance

- **Lazy Loading**: Products are loaded in pages
- **Efficient Filtering**: Client-side filtering for fast response
- **Optimized Charts**: Chart.js with responsive options
- **Minimal Dependencies**: Only essential libraries included

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py`: `app.run(port=5001)`

2. **Data not loading**:
   - Ensure `products.json` exists and is valid JSON
   - Check file permissions

3. **Charts not displaying**:
   - Ensure internet connection for CDN resources
   - Check browser console for JavaScript errors

### Debug Mode
The application runs in debug mode by default. For production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Contributing

Feel free to enhance the UI with:
- Additional chart types
- More filtering options
- Enhanced export functionality
- Mobile app version
- Dark/light theme toggle

## License

This project is part of the Iden challenge and follows the same licensing terms.
