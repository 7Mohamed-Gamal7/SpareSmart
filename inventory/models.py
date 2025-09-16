from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    """Product categories"""
    VEHICLE_TYPE_CHOICES = [
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('tuktuk', 'Tuk-Tuk'),
        ('general', 'General'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, default='general')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_vehicle_type_display()})"
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'فئة'
        verbose_name_plural = 'الفئات'
        ordering = ['vehicle_type', 'name']

class Brand(models.Model):
    """Product brands/manufacturers"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'
        verbose_name = 'علامة تجارية'
        verbose_name_plural = 'العلامات التجارية'
        ordering = ['name']

class Unit(models.Model):
    """Product units of measurement"""
    name = models.CharField(max_length=50, unique=True, verbose_name='اسم الوحدة')
    name_arabic = models.CharField(max_length=50, verbose_name='الاسم بالعربية')
    abbreviation = models.CharField(max_length=10, verbose_name='الاختصار')
    description = models.TextField(blank=True, verbose_name='الوصف')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name_arabic} ({self.abbreviation})"

    class Meta:
        db_table = 'units'
        verbose_name = 'وحدة قياس'
        verbose_name_plural = 'وحدات القياس'
        ordering = ['name_arabic']

class Supplier(models.Model):
    """Suppliers/vendors"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    tax_number = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'suppliers'
        verbose_name = 'مورد'
        verbose_name_plural = 'الموردين'
        ordering = ['name']

class Customer(models.Model):
    """العملاء"""
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('dealer', 'Dealer'),
    ]
    
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    tax_number = models.CharField(max_length=50, blank=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_customer_type_display()})"
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'عميل'
        verbose_name_plural = 'العملاء'
        ordering = ['name']

class Product(models.Model):
    """Products/spare parts"""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    barcode = models.CharField(max_length=100, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products')
    
    # Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Stock information
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    maximum_stock = models.IntegerField(default=1000)
    reorder_level = models.IntegerField(default=10)
    
    # Product specifications
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    Dimensions = models.CharField(max_length=100, blank=True)  # L x W x H
    color = models.CharField(max_length=50, blank=True)
    materials = models.CharField(max_length=100, blank=True)
    
    # Images and files
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    datasheet = models.FileField(upload_to='datasheets/', blank=True, null=True)
    
    # Compatibility
    compatible_vehicles = models.TextField(blank=True, help_text="List of compatible vehicle models")
    part_number = models.CharField(max_length=100, blank=True)
    oem_number = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def profit_margin(self):
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    @property
    def stock_status(self):
        if self.current_stock <= 0:
            return 'out_of_stock'
        elif self.current_stock <= self.reorder_level:
            return 'low_stock'
        elif self.current_stock <= self.minimum_stock:
            return 'minimum'
        return 'in_stock'
    
    @property
    def total_value(self):
        return self.current_stock * self.cost_price
    
    class Meta:
        db_table = 'products'
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['name']

class StockMovement(models.Model):
    """Track all stock movements"""
    MOVEMENT_TYPE_CHOICES = [
        ('purchase', 'شراء'),
        ('sale', 'بيع'),
        ('return_in', 'Return In'),
        ('return_out', 'Return Out'),
        ('adjustment', 'Stock Adjustment'),
        ('transfer', 'Transfer'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference_number = models.CharField(max_length=100, blank=True)
    reference_model = models.CharField(max_length=50, blank=True)  # Related model (Sale, Purchase, etc.)
    reference_id = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"
    
    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']

class InventoryAlert(models.Model):
    """Inventory alerts for low stock, etc."""
    ALERT_TYPE_CHOICES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('reorder', 'Reorder Required'),
        ('overstock', 'Overstock'),
        ('expiry', 'Expiry Alert'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    current_stock = models.IntegerField()
    recommended_action = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    acknowledged_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, blank=True, null=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.get_alert_type_display()}"
    
    class Meta:
        db_table = 'inventory_alerts'
        verbose_name = 'Inventory Alert'
        verbose_name_plural = 'Inventory Alerts'
        ordering = ['-created_at']

class ShopSettings(models.Model):
    """إعدادات المحل التجاري العامة"""
    shop_name = models.CharField(max_length=200, verbose_name='اسم المحل')
    shop_name_english = models.CharField(max_length=200, blank=True, verbose_name='اسم المحل بالإنجليزية')
    logo = models.ImageField(upload_to='shop/', blank=True, null=True, verbose_name='شعار المحل')

    # Contact Information
    phone = models.CharField(max_length=20, blank=True, verbose_name='رقم الهاتف')
    mobile = models.CharField(max_length=20, blank=True, verbose_name='رقم الموبايل')
    email = models.EmailField(blank=True, verbose_name='البريد الإلكتروني')
    website = models.URLField(blank=True, verbose_name='الموقع الإلكتروني')

    # Address Information
    address = models.TextField(blank=True, verbose_name='العنوان')
    city = models.CharField(max_length=100, blank=True, verbose_name='المدينة')
    state = models.CharField(max_length=100, blank=True, verbose_name='المحافظة')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='الرمز البريدي')
    country = models.CharField(max_length=100, default='مصر', verbose_name='البلد')

    # Business Information
    tax_number = models.CharField(max_length=50, blank=True, verbose_name='الرقم الضريبي')
    commercial_register = models.CharField(max_length=50, blank=True, verbose_name='السجل التجاري')
    license_number = models.CharField(max_length=50, blank=True, verbose_name='رقم الترخيص')

    # Invoice Settings
    invoice_prefix = models.CharField(max_length=10, default='INV', verbose_name='بادئة رقم الفاتورة')
    invoice_footer = models.TextField(blank=True, verbose_name='تذييل الفاتورة')
    terms_and_conditions = models.TextField(blank=True, verbose_name='الشروط والأحكام')

    # Currency and Format
    currency_symbol = models.CharField(max_length=10, default='ج.م', verbose_name='رمز العملة')
    currency_name = models.CharField(max_length=50, default='جنيه مصري', verbose_name='اسم العملة')
    date_format = models.CharField(max_length=20, default='%Y/%m/%d', verbose_name='تنسيق التاريخ')

    # System Settings
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name

    class Meta:
        db_table = 'shop_settings'
        verbose_name = 'إعدادات المحل'
        verbose_name_plural = 'إعدادات المحل'

    @classmethod
    def get_settings(cls):
        """Get or create shop settings"""
        settings, created = cls.objects.get_or_create(
            id=1,
            defaults={
                'shop_name': 'SpareSmart',
                'shop_name_english': 'SpareSmart Auto Parts',
                'phone': '',
                'address': '',
                'city': '',
            }
        )
        return settings

class Invoice(models.Model):
    """نموذج الفواتير (بيع وشراء)"""
    INVOICE_TYPE_CHOICES = [
        ('sale', 'فاتورة بيع'),
        ('purchase', 'فاتورة شراء'),
    ]

    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('confirmed', 'مؤكدة'),
        ('paid', 'مدفوعة'),
        ('partially_paid', 'مدفوعة جزئياً'),
        ('cancelled', 'ملغية'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'نقداً'),
        ('credit', 'آجل'),
        ('bank_transfer', 'تحويل بنكي'),
        ('check', 'شيك'),
        ('card', 'بطاقة ائتمان'),
    ]

    # Basic Information
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الفاتورة')
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPE_CHOICES, verbose_name='نوع الفاتورة')
    invoice_date = models.DateField(verbose_name='تاريخ الفاتورة')
    due_date = models.DateField(blank=True, null=True, verbose_name='تاريخ الاستحقاق')

    # Customer/Supplier Information
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True, null=True,
                                related_name='invoices', verbose_name='العميل')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, blank=True, null=True,
                                related_name='invoices', verbose_name='المورد')

    # Financial Information
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='المجموع الفرعي')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='نسبة الخصم')
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='مبلغ الخصم')
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='نسبة الضريبة')
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='مبلغ الضريبة')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='المبلغ الإجمالي')
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='المبلغ المدفوع')
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='المبلغ المتبقي')

    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES,
                                     default='cash', verbose_name='طريقة الدفع')
    payment_reference = models.CharField(max_length=100, blank=True, verbose_name='مرجع الدفع')

    # Status and Notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='الحالة')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    internal_notes = models.TextField(blank=True, verbose_name='ملاحظات داخلية')

    # System Information
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_invoices', verbose_name='أنشئت بواسطة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    def __str__(self):
        return f"{self.invoice_number} - {self.get_invoice_type_display()}"

    @property
    def is_sale(self):
        return self.invoice_type == 'sale'

    @property
    def is_purchase(self):
        return self.invoice_type == 'purchase'

    @property
    def client_name(self):
        if self.is_sale and self.customer:
            return self.customer.name
        elif self.is_purchase and self.supplier:
            return self.supplier.name
        return 'غير محدد'

    def calculate_totals(self):
        """حساب إجماليات الفاتورة"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.discount_amount = (self.subtotal * self.discount_percentage) / 100
        subtotal_after_discount = self.subtotal - self.discount_amount
        self.tax_amount = (subtotal_after_discount * self.tax_percentage) / 100
        self.total_amount = subtotal_after_discount + self.tax_amount
        self.remaining_amount = self.total_amount - self.paid_amount
        self.save()

    def generate_invoice_number(self):
        """توليد رقم فاتورة تلقائي"""
        settings = ShopSettings.get_settings()
        prefix = settings.invoice_prefix

        # Get the last invoice number for this type
        last_invoice = Invoice.objects.filter(
            invoice_type=self.invoice_type,
            invoice_number__startswith=prefix
        ).order_by('-id').first()

        if last_invoice:
            try:
                last_number = int(last_invoice.invoice_number.replace(prefix, ''))
                new_number = last_number + 1
            except ValueError:
                new_number = 1
        else:
            new_number = 1

        self.invoice_number = f"{prefix}{new_number:06d}"

    class Meta:
        db_table = 'invoices'
        verbose_name = 'فاتورة'
        verbose_name_plural = 'الفواتير'
        ordering = ['-created_at']

class InvoiceItem(models.Model):
    """عناصر الفاتورة"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name='الفاتورة')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='المنتج')

    # Product details at time of invoice (for historical accuracy)
    product_name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    product_sku = models.CharField(max_length=100, verbose_name='رمز المنتج')
    unit_name = models.CharField(max_length=50, verbose_name='الوحدة')

    # Quantity and Pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='الكمية')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر الوحدة')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='نسبة الخصم')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='مبلغ الخصم')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='السعر الإجمالي')

    # Additional Information
    notes = models.TextField(blank=True, verbose_name='ملاحظات')

    def __str__(self):
        return f"{self.product_name} - {self.quantity} {self.unit_name}"

    def save(self, *args, **kwargs):
        # Store product details for historical accuracy
        if self.product:
            self.product_name = self.product.name
            self.product_sku = self.product.sku
            self.unit_name = self.product.unit.name_arabic

        # Calculate discount amount and total price
        if self.discount_percentage > 0:
            self.discount_amount = (self.unit_price * self.quantity * self.discount_percentage) / 100
        else:
            self.discount_amount = 0

        self.total_price = (self.unit_price * self.quantity) - self.discount_amount

        super().save(*args, **kwargs)

        # Update invoice totals
        if self.invoice:
            self.invoice.calculate_totals()

    class Meta:
        db_table = 'invoice_items'
        verbose_name = 'عنصر فاتورة'
        verbose_name_plural = 'عناصر الفاتورة'
        ordering = ['id']