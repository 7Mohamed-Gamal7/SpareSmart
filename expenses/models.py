from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone

class ExpenseCategory(models.Model):
    """Categories for expenses"""
    CATEGORY_TYPE_CHOICES = [
        ('operational', 'Operational'),
        ('administrative', 'Administrative'),
        ('marketing', 'Marketing'),
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('travel', 'Travel'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='operational')
    budget_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    approval_limit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"
    
    @property
    def current_month_total(self):
        from django.db.models import Sum
        current_month = timezone.now().replace(day=1)
        return self.expenses.filter(
            expense_date__gte=current_month
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    @property
    def budget_utilization(self):
        if self.budget_limit:
            current_total = self.current_month_total
            return (current_total / self.budget_limit) * 100
        return 0
    
    class Meta:
        db_table = 'expense_categories'
        verbose_name = 'Expense Category'
        verbose_name_plural = 'Expense Categories'
        ordering = ['category_type', 'name']

class Expense(models.Model):
    """Business expenses"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('credit_card', 'Credit Card'),
        ('petty_cash', 'Petty Cash'),
        ('online', 'Online Payment'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    expense_number = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='expenses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    # Status and Approval
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    requires_approval = models.BooleanField(default=False)
    
    # Dates
    expense_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    paid_date = models.DateField(blank=True, null=True)
    
    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    vendor_name = models.CharField(max_length=200, blank=True)
    vendor_contact = models.CharField(max_length=100, blank=True)
    
    # Tax and Accounting
    is_tax_deductible = models.BooleanField(default=False)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_code = models.CharField(max_length=50, blank=True)
    
    # Documentation
    receipt_image = models.ImageField(upload_to='expense_receipts/', blank=True, null=True)
    invoice_file = models.FileField(upload_to='expense_invoices/', blank=True, null=True)
    additional_documents = models.FileField(upload_to='expense_docs/', blank=True, null=True)
    
    # Tracking and Approval
    requested_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='requested_expenses')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='approved_expenses', blank=True, null=True)
    paid_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='paid_expenses', blank=True, null=True)
    
    approval_date = models.DateTimeField(blank=True, null=True)
    approval_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    is_recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=20, blank=True)  # monthly, weekly, yearly
    next_due_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Expense #{self.expense_number} - {self.title} ({self.amount})"
    
    def save(self, *args, **kwargs):
        # Auto-generate expense number if not provided
        if not self.expense_number:
            last_expense = Expense.objects.filter(
                expense_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_expense and last_expense.expense_number:
                try:
                    last_number = int(last_expense.expense_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.expense_number = f"EXP-{timezone.now().year}-{new_number:06d}"
        
        # Check if requires approval based on category or amount
        if self.category.requires_approval or (
            self.category.approval_limit and self.amount > self.category.approval_limit
        ):
            self.requires_approval = True
        
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'expenses'
        verbose_name = 'مصروف'
        verbose_name_plural = 'المصروفات'
        ordering = ['-expense_date', '-created_at']

class RecurringExpense(models.Model):
    """Template for recurring expenses"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Schedule
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    next_due_date = models.DateField()
    last_generated_date = models.DateField(blank=True, null=True)
    
    # Settings
    auto_generate = models.BooleanField(default=True)
    auto_approve = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Details
    vendor_name = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length=20, choices=Expense.PAYMENT_METHOD_CHOICES, blank=True)
    account_code = models.CharField(max_length=50, blank=True)
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_frequency_display()}"
    
    def generate_next_expense(self):
        """Generate the next expense based on this template"""
        if self.status == 'active' and self.next_due_date <= timezone.now().date():
            expense = Expense.objects.create(
                category=self.category,
                title=self.name,
                description=self.description,
                amount=self.amount,
                expense_date=self.next_due_date,
                vendor_name=self.vendor_name,
                payment_method=self.payment_method,
                account_code=self.account_code,
                requested_by=self.created_by,
                is_recurring=True,
                status='approved' if self.auto_approve else 'pending'
            )
            
            # Update next due date
            from dateutil.relativedelta import relativedelta
            if self.frequency == 'daily':
                self.next_due_date += timezone.timedelta(days=1)
            elif self.frequency == 'weekly':
                self.next_due_date += timezone.timedelta(weeks=1)
            elif self.frequency == 'monthly':
                self.next_due_date += relativedelta(months=1)
            elif self.frequency == 'quarterly':
                self.next_due_date += relativedelta(months=3)
            elif self.frequency == 'yearly':
                self.next_due_date += relativedelta(years=1)
            
            self.last_generated_date = timezone.now().date()
            self.save()
            
            return expense
        return None
    
    class Meta:
        db_table = 'recurring_expenses'
        verbose_name = 'Recurring Expense'
        verbose_name_plural = 'Recurring Expenses'
        ordering = ['next_due_date']

class ExpenseApproval(models.Model):
    """Expense approval workflow"""
    ACTION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned for Revision'),
    ]
    
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='approvals')
    approver = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comments = models.TextField(blank=True)
    approval_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.expense.expense_number} - {self.get_action_display()} by {self.approver.username}"
    
    class Meta:
        db_table = 'expense_approvals'
        verbose_name = 'Expense Approval'
        verbose_name_plural = 'Expense Approvals'
        ordering = ['-approval_date']

class PettyCash(models.Model):
    """Petty cash management"""
    TRANSACTION_TYPE_CHOICES = [
        ('opening', 'Opening Balance'),
        ('addition', 'Cash Addition'),
        ('expense', 'Expense Payment'),
        ('return', 'Cash Return'),
        ('reconciliation', 'Reconciliation'),
    ]
    
    transaction_number = models.CharField(max_length=50, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    # Related expense if applicable
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, blank=True, null=True, related_name='petty_cash_transactions')
    
    # Tracking
    handled_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    transaction_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Petty Cash #{self.transaction_number} - {self.get_transaction_type_display()}"
    
    def save(self, *args, **kwargs):
        # Auto-generate transaction number if not provided
        if not self.transaction_number:
            last_transaction = PettyCash.objects.filter(
                transaction_date__year=timezone.now().year
            ).order_by('id').last()
            
            if last_transaction and last_transaction.transaction_number:
                try:
                    last_number = int(last_transaction.transaction_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            
            self.transaction_number = f"PC-{timezone.now().year}-{new_number:06d}"
        
        super().save(*args, **kwargs)
    
    @classmethod
    def get_current_balance(cls):
        """Get the current petty cash balance"""
        last_transaction = cls.objects.order_by('-transaction_date').first()
        return last_transaction.balance_after if last_transaction else 0
    
    class Meta:
        db_table = 'petty_cash'
        verbose_name = 'Petty Cash Transaction'
        verbose_name_plural = 'Petty Cash Transactions'
        ordering = ['-transaction_date']