from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class Sale(models.Model):
    """Sales transactions"""
    SALE_TYPE_CHOICES = [
        ('cash', 'Cash Sale'),
        ('credit', 'Credit Sale'),
        ('installment', 'Installment Sale'),
        ('wholesale', 'Wholesale'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partial_refund', 'Partial Refund'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
        ('overdue', 'Overdue'),
    ]
    
    # Basic Information
    sale_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey('inventory.Customer', on_delete=models.PROTECT, related_name='sales')
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    
    # Financial Information
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Dates
    sale_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='created_sales')
    updated_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='updated_sales', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sale #{self.sale_number} - {self.customer.name}"
    
    @property
    def profit(self):
        total_profit = 0
        for item in self.items.all():
            total_profit += item.profit
        return total_profit
    
    def save(self, *args, **kwargs):
        # Auto-generate sale number if not provided
        if not self.sale_number:
            last_sale = Sale.objects.filter(
                sale_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_sale and last_sale.sale_number:
                try:
                    last_number = int(last_sale.sale_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.sale_number = f"SAL-{timezone.now().year}-{new_number:06d}"
        
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
        if self.due_date and self.due_date < timezone.now().date() and self.balance_amount > 0:
            self.payment_status = 'overdue'
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'sales'
        verbose_name = 'بيع'
        verbose_name_plural = 'المبيعات'
        ordering = ['-created_at']

class SaleItem(models.Model):
    """Individual items in a sale"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def profit(self):
        return (self.unit_price - self.cost_price) * self.quantity
    
    def save(self, *args, **kwargs):
        # Calculate total price
        discount_amt = (self.unit_price * self.quantity * self.discount_percentage) / 100
        self.discount_amount = discount_amt
        self.total_price = (self.unit_price * self.quantity) - discount_amt
        
        # Set cost price from product if not provided
        if not self.cost_price:
            self.cost_price = self.product.cost_price
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'sale_items'
        verbose_name = 'Sale Item'
        verbose_name_plural = 'Sale Items'

class Payment(models.Model):
    """Payment records for sales"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('mobile_payment', 'Mobile Payment'),
        ('credit', 'Store Credit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='payments')
    payment_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True)
    
    # Payment details
    received_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    payment_date = models.DateTimeField(default=timezone.now)
    bank_name = models.CharField(max_length=100, blank=True)
    check_number = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment #{self.payment_number} - {self.amount}"
    
    def save(self, *args, **kwargs):
        # Auto-generate payment number if not provided
        if not self.payment_number:
            last_payment = Payment.objects.filter(
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
            
            self.payment_number = f"PAY-{timezone.now().year}-{new_number:06d}"
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'دفعة'
        verbose_name_plural = 'الدفعات'
        ordering = ['-created_at']

class Installment(models.Model):
    """Installment plans for sales"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('defaulted', 'Defaulted'),
        ('cancelled', 'Cancelled'),
    ]
    
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, related_name='installment_plan')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    installment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    number_of_installments = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Installment Plan for Sale #{self.sale.sale_number}"
    
    @property
    def paid_installments(self):
        return self.installment_payments.filter(status='paid').count()
    
    @property
    def remaining_installments(self):
        return self.number_of_installments - self.paid_installments
    
    @property
    def total_paid(self):
        return self.installment_payments.filter(status='paid').aggregate(
            total=models.Sum('amount'))['total'] or 0
    
    @property
    def remaining_balance(self):
        return self.total_amount - self.total_paid
    
    class Meta:
        db_table = 'installments'
        verbose_name = 'Installment Plan'
        verbose_name_plural = 'Installment Plans'

class InstallmentPayment(models.Model):
    """Individual installment payments"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partial', 'Partially Paid'),
        ('skipped', 'Skipped'),
    ]
    
    installment_plan = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='installment_payments')
    installment_number = models.IntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    
    received_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Installment #{self.installment_number} - {self.installment_plan.sale.sale_number}"
    
    def save(self, *args, **kwargs):
        # Check if overdue
        if self.due_date < timezone.now().date() and self.status == 'pending':
            self.status = 'overdue'
        
        # Update status based on payment
        if self.paid_amount >= self.amount:
            self.status = 'paid'
            if not self.paid_date:
                self.paid_date = timezone.now().date()
        elif self.paid_amount > 0:
            self.status = 'partial'
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'installment_payments'
        verbose_name = 'Installment Payment'
        verbose_name_plural = 'Installment Payments'
        ordering = ['installment_number']
        unique_together = ['installment_plan', 'installment_number']