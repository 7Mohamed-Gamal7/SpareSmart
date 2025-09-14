# SpareSmart - Spare Parts Management System

![SpareSmart Logo](https://via.placeholder.com/200x100/2c3e50/white?text=SpareSmart)

## Overview

SpareSmart is a comprehensive web application for managing spare parts stores, specifically designed for motorcycle, car, and tuk-tuk spare parts businesses. The system provides complete business management functionality including inventory management, sales tracking, purchase management, expense tracking, installment systems, and comprehensive reporting.

## Features

### 🔐 Authentication & Authorization
- Professional login system with role-based access control
- User roles: Admin, Manager, Sales Representative, Cashier, Viewer
- Granular permission system for different modules
- User profile management with detailed information

### 📊 Professional Dashboard
- Real-time business metrics and KPI cards
- Interactive charts and graphs
- Quick action buttons for common tasks
- System alerts and notifications
- Activity logging and tracking

### 📦 Inventory Management
- Product catalog with detailed specifications
- Category management by vehicle type (Motorcycle, Car, Tuk-Tuk)
- Brand management
- Stock level tracking with automated alerts
- Low stock and out-of-stock notifications
- Stock movement history

### 👥 Customer & Supplier Management
- Customer database with credit limit tracking
- Supplier management with payment terms
- Customer types: Individual, Business, Dealer
- Contact information and transaction history

### 💰 Sales System
- Point of sale interface
- Invoice generation and printing
- Multiple payment methods
- Credit sales with payment tracking
- Installment sales with automated reminders
- Sale returns and refunds

### 🚚 Purchase Management
- Purchase order creation and management
- Supplier invoice tracking
- Goods receiving with quality control
- Purchase payments and reconciliation
- Purchase returns to suppliers

### 💸 Expense Tracking
- Expense categorization by type
- Approval workflow for expenses
- Recurring expense automation
- Petty cash management
- Budget tracking and alerts

### 📈 Comprehensive Reporting
- Sales reports with date ranges
- Purchase analysis reports
- Expense reports by category
- Inventory valuation reports
- Profit & Loss statements
- Customer statement generation
- Aging reports for receivables
- Custom report builder

### 🔔 Automation & Alerts
- Daily sales and expense summaries
- Weekly installment reports
- Monthly inventory analysis
- Low stock notifications
- Payment due reminders
- System maintenance alerts

## Technology Stack

### Backend
- **Django 4.2.7** - Python web framework
- **Python 3.11+** - Programming language
- **SQLite** (Development) / **SQL Server** (Production) - Database
- **Django REST Framework** - API development

### Frontend
- **Bootstrap 5.3** - UI framework
- **Chart.js** - Interactive charts
- **Font Awesome 6.4** - Icons
- **DataTables** - Advanced table functionality
- **jQuery 3.7** - JavaScript library

### Additional Tools
- **Django Crispy Forms** - Form rendering
- **ReportLab** - PDF generation
- **XlsxWriter** - Excel export
- **Pillow** - Image processing

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/7Mohamed-Gamal7/SpareSmart.git
cd SpareSmart
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your settings
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Initialize system with default data**
```bash
python manage.py init_system --create-superuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the application**
- URL: `http://127.0.0.1:8000`
- Default credentials: `admin` / `admin123`

## Database Configuration

### Development (SQLite)
The application is configured to use SQLite for development by default.

### Production (SQL Server)
To use SQL Server in production, update the database configuration in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'sparesmart_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'your_server',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
            'autocommit': True,
        },
    }
}
```

## System Modules

### 1. Accounts Module
- User authentication and authorization
- Role-based permission system
- User profile management
- Activity logging

### 2. Inventory Module
- Product management
- Category and brand management
- Stock tracking and alerts
- Supplier and customer management

### 3. Sales Module
- Point of sale system
- Invoice generation
- Payment processing
- Installment management

### 4. Purchases Module
- Purchase order management
- Goods receiving
- Supplier payments
- Return processing

### 5. Expenses Module
- Expense recording and categorization
- Approval workflows
- Recurring expenses
- Petty cash management

### 6. Reports Module
- Pre-built report templates
- Custom report builder
- Export functionality (PDF, Excel)
- Scheduled reports

### 7. Dashboard Module
- Business metrics dashboard
- System notifications
- User preferences
- Activity monitoring

## User Roles & Permissions

### Admin
- Full system access
- User management
- System configuration
- All module permissions

### Manager
- Most system functions
- User management (limited)
- Approval permissions
- All reports access

### Sales Representative
- Sales creation and management
- Customer management
- Payment processing
- Sales reports

### Cashier
- Point of sale access
- Payment processing
- Limited product view
- Basic sales functions

### Viewer
- Read-only access
- Basic reports
- Dashboard view
- No modification permissions

## Default Data

The system includes default data for quick setup:

- **Product Categories**: Organized by vehicle type
- **Brands**: Major automotive brands
- **Expense Categories**: Common business expense types
- **Permissions**: Comprehensive permission set
- **System Configuration**: Basic business settings

## API Documentation

The system provides RESTful APIs for integration:

- Authentication endpoints
- Inventory management APIs
- Sales and purchase APIs
- Reporting APIs
- Real-time notifications

## Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password hashing
- Session management
- Role-based access control

## Performance Features

- Database query optimization
- Pagination for large datasets
- Efficient search functionality
- Caching implementation
- Static file optimization

## N8N Automation Integration

The system is designed to integrate with N8N for workflow automation:

- Automated report generation
- Email notifications
- Inventory alerts
- Payment reminders
- Business intelligence workflows

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For support and questions:
- Create an issue on GitHub
- Email: support@sparesmart.com
- Documentation: [Wiki](https://github.com/7Mohamed-Gamal7/SpareSmart/wiki)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Version 2.0 (Planned)
- Mobile application
- Advanced analytics
- Multi-location support
- E-commerce integration
- Barcode scanning
- Advanced workflow automation

### Version 1.1 (In Progress)
- Complete inventory management
- Full sales system implementation
- Purchase system completion
- Advanced reporting features
- N8N workflow templates

## Screenshots

### Login Screen
Professional login interface with system features overview.

### Dashboard
Real-time business metrics with interactive charts and quick actions.

### Inventory Management
Comprehensive product catalog with advanced filtering and search.

### Sales Interface
Point of sale system with invoice generation capabilities.

### Reports
Professional reports with export functionality and scheduling.

---

**SpareSmart** - Streamlining spare parts business management since 2024.

For more information, visit our [GitHub repository](https://github.com/7Mohamed-Gamal7/SpareSmart).