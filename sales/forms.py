from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from .models import Sale, SaleItem, Payment, Installment, InstallmentPayment
from inventory.models import Product, Customer
from accounts.models import User

class SaleForm(forms.ModelForm):
    """Form for creating and editing sales"""
    
    class Meta:
        model = Sale
        fields = [
            'customer', 'sale_type', 'sale_date', 'due_date', 
            'discount_amount', 'notes', 'internal_notes'
        ]
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'sale_type': forms.Select(attrs={'class': 'form-select'}),
            'sale_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'discount_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(is_active=True).order_by('name')
        self.fields['customer'].empty_label = "Select a customer"
        
        # Make certain fields required
        self.fields['customer'].required = True
        self.fields['sale_date'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        sale_type = cleaned_data.get('sale_type')
        due_date = cleaned_data.get('due_date')
        
        # If credit sale, due date is required
        if sale_type in ['credit', 'installment'] and not due_date:
            raise ValidationError("Due date is required for credit and installment sales.")
        
        return cleaned_data

class SaleItemForm(forms.ModelForm):
    """Form for adding items to a sale"""
    
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'unit_price', 'discount_percentage']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True, current_stock__gt=0).order_by('name')
        self.fields['product'].empty_label = "Select a product"
        
        # Set default values
        if self.instance.pk and self.instance.product:
            self.fields['unit_price'].initial = self.instance.product.selling_price
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')
        discount_percentage = cleaned_data.get('discount_percentage', 0)
        
        if product and quantity:
            # Check stock availability
            if quantity > product.current_stock:
                raise ValidationError(f"Insufficient stock. Available: {product.current_stock}")
        
        if unit_price and discount_percentage:
            if discount_percentage > 100:
                raise ValidationError("Discount percentage cannot exceed 100%")
        
        return cleaned_data

class SaleItemFormSet(forms.BaseInlineFormSet):
    """Formset for managing sale items"""
    
    def clean(self):
        super().clean()
        
        if any(self.errors):
            return
        
        # Check that at least one item is being sold
        forms_data = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                forms_data.append(form.cleaned_data)
        
        if not forms_data:
            raise ValidationError("At least one item must be added to the sale.")

# Create the actual formset
SaleItemInlineFormSet = forms.inlineformset_factory(
    Sale, SaleItem, form=SaleItemForm, formset=SaleItemFormSet,
    extra=1, min_num=1, validate_min=True, can_delete=True
)

class PaymentForm(forms.ModelForm):
    """Form for recording payments"""
    
    class Meta:
        model = Payment
        fields = [
            'amount', 'payment_method', 'reference_number', 
            'notes', 'bank_name', 'check_number'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
            'check_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.sale = kwargs.pop('sale', None)
        super().__init__(*args, **kwargs)
        
        if self.sale:
            # Set maximum amount to remaining balance
            max_amount = self.sale.balance_amount
            self.fields['amount'].widget.attrs['max'] = str(max_amount)
            self.fields['amount'].initial = max_amount
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        
        if self.sale and amount > self.sale.balance_amount:
            raise ValidationError(f"Payment amount cannot exceed remaining balance of ${self.sale.balance_amount}")
        
        return amount

class InstallmentPlanForm(forms.ModelForm):
    """Form for creating installment plans"""
    
    class Meta:
        model = Installment
        fields = [
            'down_payment', 'installment_amount', 'number_of_installments',
            'interest_rate', 'start_date'
        ]
        widgets = {
            'down_payment': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'installment_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'number_of_installments': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.sale = kwargs.pop('sale', None)
        super().__init__(*args, **kwargs)
        
        if self.sale:
            self.fields['down_payment'].widget.attrs['max'] = str(self.sale.total_amount)
    
    def clean(self):
        cleaned_data = super().clean()
        down_payment = cleaned_data.get('down_payment', 0)
        installment_amount = cleaned_data.get('installment_amount')
        number_of_installments = cleaned_data.get('number_of_installments')
        
        if self.sale:
            if down_payment >= self.sale.total_amount:
                raise ValidationError("Down payment cannot be equal to or greater than total amount.")
            
            if installment_amount and number_of_installments:
                total_installments = installment_amount * number_of_installments
                remaining_amount = self.sale.total_amount - down_payment
                
                if total_installments < remaining_amount * 0.9:  # Allow 10% tolerance
                    raise ValidationError("Total installment amount is too low for the remaining balance.")
        
        return cleaned_data

class SaleFilterForm(forms.Form):
    """Form for filtering sales"""
    
    SEARCH_CHOICES = [
        ('', 'All Sales'),
        ('today', 'Today'),
        ('yesterday', 'Yesterday'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('last_month', 'Last Month'),
    ]
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by sale number, customer...'})
    )
    
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_active=True).order_by('name'),
        required=False,
        empty_label="All Customers",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    sale_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Sale.SALE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Sale.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    payment_status = forms.ChoiceField(
        choices=[('', 'All Payment Status')] + Sale.PAYMENT_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_range = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise ValidationError("Start date cannot be later than end date.")
        
        return cleaned_data

class QuickSaleForm(forms.Form):
    """Quick sale form for simple cash transactions"""
    
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_active=True).order_by('name'),
        required=True,
        empty_label="Select Customer",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True, current_stock__gt=0).order_by('name'),
        required=True,
        empty_label="Select Product",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    unit_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    discount_percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0,
        max_value=100,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        initial='cash',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product and quantity:
            if quantity > product.current_stock:
                raise ValidationError(f"Insufficient stock for {product.name}. Available: {product.current_stock}")
        
        return cleaned_data
    
    def create_sale(self, user):
        """Create a quick sale with payment"""
        with transaction.atomic():
            # Create the sale
            sale = Sale.objects.create(
                customer=self.cleaned_data['customer'],
                sale_type='cash',
                status='completed',
                created_by=user
            )
            
            # Create sale item
            unit_price = self.cleaned_data['unit_price']
            quantity = self.cleaned_data['quantity']
            discount_percentage = self.cleaned_data.get('discount_percentage', 0)
            
            sale_item = SaleItem.objects.create(
                sale=sale,
                product=self.cleaned_data['product'],
                quantity=quantity,
                unit_price=unit_price,
                discount_percentage=discount_percentage
            )
            
            # Update sale totals
            sale.subtotal = sale_item.total_price
            sale.total_amount = sale_item.total_price
            sale.save()
            
            # Create payment
            payment = Payment.objects.create(
                sale=sale,
                amount=sale.total_amount,
                payment_method=self.cleaned_data['payment_method'],
                received_by=user
            )
            
            # Update product stock
            product = self.cleaned_data['product']
            product.current_stock -= quantity
            product.save()
            
            return sale

class InstallmentPaymentForm(forms.ModelForm):
    """Form for recording installment payments"""
    
    class Meta:
        model = InstallmentPayment
        fields = ['paid_amount', 'notes']
        widgets = {
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            remaining_amount = self.instance.amount - self.instance.paid_amount
            self.fields['paid_amount'].widget.attrs['max'] = str(remaining_amount)
            self.fields['paid_amount'].initial = remaining_amount
    
    def clean_paid_amount(self):
        paid_amount = self.cleaned_data['paid_amount']
        
        if self.instance.pk:
            remaining_amount = self.instance.amount - self.instance.paid_amount
            if paid_amount > remaining_amount:
                raise ValidationError(f"Payment amount cannot exceed remaining balance of ${remaining_amount}")
        
        return paid_amount