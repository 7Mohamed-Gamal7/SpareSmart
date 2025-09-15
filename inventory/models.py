from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

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
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        ordering = ['name']

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
    UNIT_CHOICES = [
        ('piece', 'Piece'),
        ('set', 'Set'),
        ('pair', 'Pair'),
        ('meter', 'Meter'),
        ('liter', 'Liter'),
        ('kg', 'Kilogram'),
        ('box', 'Box'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    barcode = models.CharField(max_length=100, blank=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', blank=True, null=True)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='piece')
    
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