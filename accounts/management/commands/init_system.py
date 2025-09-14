from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Permission, RolePermission
from inventory.models import Category, Brand
from expenses.models import ExpenseCategory
from dashboard.models import SystemConfiguration

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize the SpareSmart system with default data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a default superuser',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing SpareSmart system...'))

        # Create default permissions
        self.create_permissions()
        
        # Create default role permissions
        self.create_role_permissions()
        
        # Create default categories
        self.create_categories()
        
        # Create default brands
        self.create_brands()
        
        # Create default expense categories
        self.create_expense_categories()
        
        # Create system configuration
        self.create_system_config()
        
        # Create superuser if requested
        if options['create_superuser']:
            self.create_superuser()

        self.stdout.write(self.style.SUCCESS('System initialization completed successfully!'))

    def create_permissions(self):
        """Create default permissions"""
        permissions = [
            # Inventory permissions
            {'name': 'View Products', 'codename': 'view_products', 'module': 'inventory'},
            {'name': 'Add Products', 'codename': 'add_products', 'module': 'inventory'},
            {'name': 'Edit Products', 'codename': 'edit_products', 'module': 'inventory'},
            {'name': 'Delete Products', 'codename': 'delete_products', 'module': 'inventory'},
            {'name': 'Manage Categories', 'codename': 'manage_categories', 'module': 'inventory'},
            {'name': 'View Stock Reports', 'codename': 'view_stock_reports', 'module': 'inventory'},
            
            # Sales permissions
            {'name': 'View Sales', 'codename': 'view_sales', 'module': 'sales'},
            {'name': 'Create Sales', 'codename': 'create_sales', 'module': 'sales'},
            {'name': 'Edit Sales', 'codename': 'edit_sales', 'module': 'sales'},
            {'name': 'Delete Sales', 'codename': 'delete_sales', 'module': 'sales'},
            {'name': 'Process Payments', 'codename': 'process_payments', 'module': 'sales'},
            {'name': 'Manage Installments', 'codename': 'manage_installments', 'module': 'sales'},
            
            # Purchases permissions
            {'name': 'View Purchases', 'codename': 'view_purchases', 'module': 'purchases'},
            {'name': 'Create Purchases', 'codename': 'create_purchases', 'module': 'purchases'},
            {'name': 'Edit Purchases', 'codename': 'edit_purchases', 'module': 'purchases'},
            {'name': 'Delete Purchases', 'codename': 'delete_purchases', 'module': 'purchases'},
            {'name': 'Approve Purchases', 'codename': 'approve_purchases', 'module': 'purchases'},
            
            # Expenses permissions
            {'name': 'View Expenses', 'codename': 'view_expenses', 'module': 'expenses'},
            {'name': 'Create Expenses', 'codename': 'create_expenses', 'module': 'expenses'},
            {'name': 'Edit Expenses', 'codename': 'edit_expenses', 'module': 'expenses'},
            {'name': 'Approve Expenses', 'codename': 'approve_expenses', 'module': 'expenses'},
            {'name': 'Manage Petty Cash', 'codename': 'manage_petty_cash', 'module': 'expenses'},
            
            # Reports permissions
            {'name': 'View Reports', 'codename': 'view_reports', 'module': 'reports'},
            {'name': 'Generate Reports', 'codename': 'generate_reports', 'module': 'reports'},
            {'name': 'Schedule Reports', 'codename': 'schedule_reports', 'module': 'reports'},
            {'name': 'Export Data', 'codename': 'export_data', 'module': 'reports'},
            
            # Users permissions
            {'name': 'View Users', 'codename': 'view_users', 'module': 'users'},
            {'name': 'Create Users', 'codename': 'create_users', 'module': 'users'},
            {'name': 'Edit Users', 'codename': 'edit_users', 'module': 'users'},
            {'name': 'Delete Users', 'codename': 'delete_users', 'module': 'users'},
            {'name': 'Manage Permissions', 'codename': 'manage_permissions', 'module': 'users'},
            
            # System permissions
            {'name': 'System Configuration', 'codename': 'system_config', 'module': 'system'},
            {'name': 'View Logs', 'codename': 'view_logs', 'module': 'system'},
            {'name': 'Backup System', 'codename': 'backup_system', 'module': 'system'},
        ]

        for perm_data in permissions:
            permission, created = Permission.objects.get_or_create(
                codename=perm_data['codename'],
                defaults=perm_data
            )
            if created:
                self.stdout.write(f'Created permission: {permission.name}')

    def create_role_permissions(self):
        """Create default role permissions"""
        # Admin - all permissions
        admin_permissions = Permission.objects.all()
        for permission in admin_permissions:
            RolePermission.objects.get_or_create(role='admin', permission=permission)

        # Manager permissions
        manager_perms = [
            'view_products', 'add_products', 'edit_products', 'manage_categories', 'view_stock_reports',
            'view_sales', 'create_sales', 'edit_sales', 'process_payments', 'manage_installments',
            'view_purchases', 'create_purchases', 'edit_purchases', 'approve_purchases',
            'view_expenses', 'create_expenses', 'edit_expenses', 'approve_expenses', 'manage_petty_cash',
            'view_reports', 'generate_reports', 'schedule_reports', 'export_data',
            'view_users', 'create_users', 'edit_users', 'view_logs'
        ]
        for codename in manager_perms:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(role='manager', permission=permission)
            except Permission.DoesNotExist:
                pass

        # Sales permissions
        sales_perms = [
            'view_products', 'view_stock_reports',
            'view_sales', 'create_sales', 'edit_sales', 'process_payments', 'manage_installments',
            'view_reports', 'generate_reports'
        ]
        for codename in sales_perms:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(role='sales', permission=permission)
            except Permission.DoesNotExist:
                pass

        # Cashier permissions
        cashier_perms = [
            'view_products', 'view_sales', 'create_sales', 'process_payments'
        ]
        for codename in cashier_perms:
            try:
                permission = Permission.objects.get(codename=codename)
                RolePermission.objects.get_or_create(role='cashier', permission=permission)
            except Permission.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS('Created default role permissions'))

    def create_categories(self):
        """Create default product categories"""
        categories = [
            {'name': 'Motorcycle Engine Parts', 'vehicle_type': 'motorcycle', 'description': 'Engine components for motorcycles'},
            {'name': 'Car Engine Parts', 'vehicle_type': 'car', 'description': 'Engine components for cars'},
            {'name': 'Tuk-Tuk Engine Parts', 'vehicle_type': 'tuktuk', 'description': 'Engine components for tuk-tuks'},
            {'name': 'Motorcycle Brake System', 'vehicle_type': 'motorcycle', 'description': 'Brake components for motorcycles'},
            {'name': 'Car Brake System', 'vehicle_type': 'car', 'description': 'Brake components for cars'},
            {'name': 'Motorcycle Electrical', 'vehicle_type': 'motorcycle', 'description': 'Electrical components for motorcycles'},
            {'name': 'Car Electrical', 'vehicle_type': 'car', 'description': 'Electrical components for cars'},
            {'name': 'Motorcycle Body Parts', 'vehicle_type': 'motorcycle', 'description': 'Body components for motorcycles'},
            {'name': 'Car Body Parts', 'vehicle_type': 'car', 'description': 'Body components for cars'},
            {'name': 'Filters', 'vehicle_type': 'general', 'description': 'Oil, air, and fuel filters'},
            {'name': 'Oils & Lubricants', 'vehicle_type': 'general', 'description': 'Engine oils and lubricants'},
            {'name': 'Tools & Equipment', 'vehicle_type': 'general', 'description': 'Repair tools and equipment'},
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name} ({category.get_vehicle_type_display()})')

    def create_brands(self):
        """Create default brands"""
        brands = [
            'Honda', 'Yamaha', 'Suzuki', 'Kawasaki', 'Toyota', 'Nissan', 'Hyundai',
            'KIA', 'Chevrolet', 'Ford', 'Volkswagen', 'BMW', 'Mercedes-Benz', 'Audi',
            'Bosch', 'NGK', 'Denso', 'Mobil', 'Shell', 'Castrol', 'Valvoline'
        ]

        for brand_name in brands:
            brand, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                self.stdout.write(f'Created brand: {brand.name}')

    def create_expense_categories(self):
        """Create default expense categories"""
        categories = [
            {'name': 'Rent', 'category_type': 'operational', 'description': 'Shop/warehouse rent'},
            {'name': 'Utilities', 'category_type': 'utilities', 'description': 'Electricity, water, internet'},
            {'name': 'Staff Salaries', 'category_type': 'operational', 'description': 'Employee salaries and wages'},
            {'name': 'Marketing', 'category_type': 'marketing', 'description': 'Advertising and marketing expenses'},
            {'name': 'Office Supplies', 'category_type': 'administrative', 'description': 'Office materials and supplies'},
            {'name': 'Equipment Maintenance', 'category_type': 'maintenance', 'description': 'Equipment repair and maintenance'},
            {'name': 'Transportation', 'category_type': 'operational', 'description': 'Vehicle fuel and transportation'},
            {'name': 'Insurance', 'category_type': 'administrative', 'description': 'Business insurance premiums'},
            {'name': 'Bank Charges', 'category_type': 'administrative', 'description': 'Banking fees and charges'},
            {'name': 'Professional Services', 'category_type': 'administrative', 'description': 'Legal, accounting, consulting'},
        ]

        for cat_data in categories:
            category, created = ExpenseCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created expense category: {category.name}')

    def create_system_config(self):
        """Create default system configuration"""
        configs = [
            {'category': 'business', 'key': 'company_name', 'value': 'SpareSmart Store', 'description': 'Company name'},
            {'category': 'business', 'key': 'company_address', 'value': 'Your Store Address', 'description': 'Company address'},
            {'category': 'business', 'key': 'company_phone', 'value': 'Your Phone Number', 'description': 'Company phone'},
            {'category': 'business', 'key': 'company_email', 'value': 'info@sparesmart.com', 'description': 'Company email'},
            {'category': 'business', 'key': 'tax_rate', 'value': '14', 'data_type': 'float', 'description': 'Default tax rate percentage'},
            {'category': 'business', 'key': 'currency', 'value': 'USD', 'description': 'Default currency'},
            {'category': 'inventory', 'key': 'low_stock_threshold', 'value': '10', 'data_type': 'integer', 'description': 'Default low stock threshold'},
            {'category': 'financial', 'key': 'fiscal_year_start', 'value': '01-01', 'description': 'Fiscal year start (MM-DD)'},
        ]

        for config_data in configs:
            config, created = SystemConfiguration.objects.get_or_create(
                category=config_data['category'],
                key=config_data['key'],
                defaults=config_data
            )
            if created:
                self.stdout.write(f'Created system config: {config.category}.{config.key}')

    def create_superuser(self):
        """Create default superuser"""
        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create_user(
                username='admin',
                email='admin@sparesmart.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                role='admin',
                is_staff=True,
                is_superuser=True,
                is_active_employee=True
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))