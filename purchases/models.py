from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class Purchase(models.Model):
    """Purchase orders and receipts"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ordered', 'Ordered'),
        ('partial_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
        ('overdue', 'Overdue'),
    ]
    
    # Basic Information
    purchase_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey('inventory.Supplier', on_delete=models.PROTECT, related_name='purchases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    
    # Financial Information
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Dates
    order_date = models.DateTimeField(default=timezone.now)
    expected_delivery_date = models.DateField(blank=True, null=True)
    actual_delivery_date = models.DateField(blank=True, null=True)
    payment_due_date = models.DateField(blank=True, null=True)
    
    # Reference Information
    supplier_invoice_number = models.CharField(max_length=100, blank=True)
    supplier_reference = models.CharField(max_length=100, blank=True)
    delivery_address = models.TextField(blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='created_purchases')
    updated_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='updated_purchases', blank=True, null=True)
    received_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='received_purchases', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Purchase #{self.purchase_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate purchase number if not provided
        if not self.purchase_number:
            last_purchase = Purchase.objects.filter(
                order_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_purchase and last_purchase.purchase_number:
                try:
                    last_number = int(last_purchase.purchase_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.purchase_number = f"PUR-{timezone.now().year}-{new_number:06d}"
        
        # Calculate balance
        self.balance_amount = self.total_amount - self.paid_amount
        
        # Update payment status
        if self.balance_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'
            
        # Check if overdue
        if self.payment_due_date and self.payment_due_date < timezone.now().date() and self.balance_amount > 0:
            self.payment_status = 'overdue'
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'purchases'
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ['-created_at']

class PurchaseItem(models.Model):
    """Individual items in a purchase order"""
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity_ordered = models.IntegerField(validators=[MinValueValidator(1)])
    quantity_received = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Quality control
    quality_check_passed = models.BooleanField(default=True)
    quality_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity_ordered}"
    
    @property
    def quantity_pending(self):
        return self.quantity_ordered - self.quantity_received
    
    @property
    def is_fully_received(self):
        return self.quantity_received >= self.quantity_ordered
    
    def save(self, *args, **kwargs):
        # Calculate total cost
        discount_amt = (self.unit_cost * self.quantity_ordered * self.discount_percentage) / 100
        self.discount_amount = discount_amt
        self.total_cost = (self.unit_cost * self.quantity_ordered) - discount_amt
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'purchase_items'
        verbose_name = 'Purchase Item'
        verbose_name_plural = 'Purchase Items'

class PurchasePayment(models.Model):
    """Payment records for purchases"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('credit_card', 'Credit Card'),
        ('trade_credit', 'Trade Credit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_payments')
    payment_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True)
    
    # Payment details
    paid_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    payment_date = models.DateTimeField(default=timezone.now)
    bank_name = models.CharField(max_length=100, blank=True)
    check_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Purchase Payment #{self.payment_number} - {self.amount}"
    
    def save(self, *args, **kwargs):
        # Auto-generate payment number if not provided
        if not self.payment_number:
            last_payment = PurchasePayment.objects.filter(
                payment_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_payment and last_payment.payment_number:
                try:
                    last_number = int(last_payment.payment_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.payment_number = f"PPAY-{timezone.now().year}-{new_number:06d}"
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'purchase_payments'
        verbose_name = 'Purchase Payment'
        verbose_name_plural = 'Purchase Payments'
        ordering = ['-created_at']

class PurchaseReturn(models.Model):
    """Returns to suppliers"""
    RETURN_TYPE_CHOICES = [
        ('defective', 'Defective Product'),
        ('wrong_item', 'Wrong Item'),
        ('excess', 'Excess Quantity'),
        ('damaged', 'Damaged in Transit'),
        ('quality', 'Quality Issues'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='returns')
    return_number = models.CharField(max_length=50, unique=True)
    return_type = models.CharField(max_length=20, choices=RETURN_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    reason = models.TextField()
    supplier_approval = models.TextField(blank=True)
    return_date = models.DateField(default=timezone.now)
    refund_date = models.DateField(blank=True, null=True)
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Return #{self.return_number} - {self.purchase.purchase_number}"
    
    def save(self, *args, **kwargs):
        # Auto-generate return number if not provided
        if not self.return_number:
            last_return = PurchaseReturn.objects.filter(
                return_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_return and last_return.return_number:
                try:
                    last_number = int(last_return.return_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.return_number = f"RET-{timezone.now().year}-{new_number:06d}"
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'purchase_returns'
        verbose_name = 'Purchase Return'
        verbose_name_plural = 'Purchase Returns'
        ordering = ['-created_at']

class PurchaseReturnItem(models.Model):
    """Items being returned to supplier"""
    return_order = models.ForeignKey(PurchaseReturn, on_delete=models.CASCADE, related_name='items')
    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Return {self.purchase_item.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.unit_cost
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'purchase_return_items'
        verbose_name = 'Purchase Return Item'
        verbose_name_plural = 'Purchase Return Items'