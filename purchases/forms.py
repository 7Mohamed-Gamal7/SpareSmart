from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Purchase, PurchaseItem, PurchasePayment
from inventory.models import Product, Supplier


class PurchaseForm(forms.ModelForm):
    """Form for creating and editing purchase orders"""

    class Meta:
        model = Purchase
        fields = [
            'supplier', 'expected_delivery_date', 'payment_due_date',
            'supplier_invoice_number', 'supplier_reference', 'delivery_address',
            'tax_amount', 'discount_amount', 'shipping_cost',
            'notes', 'internal_notes', 'terms_and_conditions'
        ]
        labels = {
            'supplier': 'المورد',
            'expected_delivery_date': 'تاريخ التسليم المتوقع',
            'payment_due_date': 'تاريخ استحقاق الدفع',
            'supplier_invoice_number': 'رقم فاتورة المورد',
            'supplier_reference': 'مرجع المورد',
            'delivery_address': 'عنوان التسليم',
            'tax_amount': 'مبلغ الضريبة',
            'discount_amount': 'مبلغ الخصم',
            'shipping_cost': 'تكلفة الشحن',
            'notes': 'ملاحظات',
            'internal_notes': 'ملاحظات داخلية',
            'terms_and_conditions': 'الشروط والأحكام',
        }
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'expected_delivery_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'payment_due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'supplier_invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم فاتورة المورد'
            }),
            'supplier_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مرجع المورد أو رقم أمر الشراء'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'عنوان التسليم (اتركه فارغاً للعنوان الافتراضي)'
            }),
            'tax_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'discount_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'shipping_cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'ملاحظات الشراء (مرئية للمورد)'
            }),
            'internal_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'ملاحظات داخلية (غير مرئية للمورد)'
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'الشروط والأحكام لهذا الشراء'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.filter(is_active=True).order_by('name')
        
        # Set default values
        if not self.instance.pk:
            self.fields['tax_amount'].initial = 0.00
            self.fields['discount_amount'].initial = 0.00
            self.fields['shipping_cost'].initial = 0.00

    def clean(self):
        cleaned_data = super().clean()

        # Validate and convert financial fields to Decimal
        from decimal import Decimal

        tax_amount = cleaned_data.get('tax_amount', 0)
        discount_amount = cleaned_data.get('discount_amount', 0)
        shipping_cost = cleaned_data.get('shipping_cost', 0)

        # Convert to Decimal for consistency
        if tax_amount is not None:
            cleaned_data['tax_amount'] = Decimal(str(tax_amount))
            if cleaned_data['tax_amount'] < 0:
                raise ValidationError("Tax amount cannot be negative.")

        if discount_amount is not None:
            cleaned_data['discount_amount'] = Decimal(str(discount_amount))
            if cleaned_data['discount_amount'] < 0:
                raise ValidationError("Discount amount cannot be negative.")

        if shipping_cost is not None:
            cleaned_data['shipping_cost'] = Decimal(str(shipping_cost))
            if cleaned_data['shipping_cost'] < 0:
                raise ValidationError("Shipping cost cannot be negative.")

        return cleaned_data


class PurchaseItemForm(forms.ModelForm):
    """Form for purchase order line items"""

    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity_ordered', 'unit_cost', 'discount_percentage']
        labels = {
            'product': 'المنتج',
            'quantity_ordered': 'الكمية المطلوبة',
            'unit_cost': 'سعر الوحدة',
            'discount_percentage': 'نسبة الخصم (%)',
        }
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select product-select',
                'required': True
            }),
            'quantity_ordered': forms.NumberInput(attrs={
                'class': 'form-control quantity-input',
                'min': '1',
                'required': True
            }),
            'unit_cost': forms.NumberInput(attrs={
                'class': 'form-control cost-input',
                'step': '0.01',
                'min': '0',
                'required': True
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-control discount-input',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(is_active=True).order_by('name')
        
        # Set default values
        if not self.instance.pk:
            self.fields['quantity_ordered'].initial = 1
            self.fields['discount_percentage'].initial = 0.00

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity_ordered')
        unit_cost = cleaned_data.get('unit_cost')
        discount = cleaned_data.get('discount_percentage', 0)
        
        if quantity and quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
            
        if unit_cost and unit_cost < 0:
            raise ValidationError("Unit cost cannot be negative.")
            
        if discount < 0 or discount > 100:
            raise ValidationError("Discount percentage must be between 0 and 100.")
        
        return cleaned_data


# Create formset for purchase items
PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)


class PurchaseReceivingForm(forms.Form):
    """Form for receiving goods against a purchase order"""
    
    def __init__(self, purchase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purchase = purchase
        
        # Create fields for each purchase item
        for item in purchase.items.all():
            pending_qty = item.quantity_pending
            if pending_qty > 0:
                field_name = f'receive_qty_{item.id}'
                self.fields[field_name] = forms.IntegerField(
                    label=f'{item.product.name}',
                    min_value=0,
                    max_value=pending_qty,
                    initial=0,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control',
                        'placeholder': f'Max: {pending_qty}'
                    })
                )
                
                # Quality check field
                quality_field_name = f'quality_check_{item.id}'
                self.fields[quality_field_name] = forms.BooleanField(
                    label=f'Quality check passed for {item.product.name}',
                    initial=True,
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                )
                
                # Quality notes field
                notes_field_name = f'quality_notes_{item.id}'
                self.fields[notes_field_name] = forms.CharField(
                    label=f'Quality notes for {item.product.name}',
                    required=False,
                    widget=forms.Textarea(attrs={
                        'class': 'form-control',
                        'rows': 2,
                        'placeholder': 'Any quality issues or notes'
                    })
                )

    def clean(self):
        cleaned_data = super().clean()
        has_received_items = False
        
        for field_name, value in cleaned_data.items():
            if field_name.startswith('receive_qty_') and value and value > 0:
                has_received_items = True
                break
        
        if not has_received_items:
            raise ValidationError("Please specify quantities to receive for at least one item.")
        
        return cleaned_data


class PurchasePaymentForm(forms.ModelForm):
    """Form for recording payments made to suppliers"""
    
    class Meta:
        model = PurchasePayment
        fields = [
            'amount', 'payment_method', 'payment_date', 'reference_number',
            'notes'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'payment_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Check number, transaction ID, etc.'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Payment notes or additional information'
            }),
        }

    def __init__(self, purchase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.purchase = purchase
        
        # Set max amount to remaining balance
        self.fields['amount'].widget.attrs['max'] = str(purchase.balance_amount)
        
        # Set default payment date to today
        from django.utils import timezone
        self.fields['payment_date'].initial = timezone.now().date()

    def clean_amount(self):
        from decimal import Decimal
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError("Payment amount must be greater than 0.")

        if amount:
            amount_decimal = Decimal(str(amount))
            balance_decimal = Decimal(str(self.purchase.balance_amount))
            if amount_decimal > balance_decimal:
                raise ValidationError(f"Payment amount cannot exceed balance of {balance_decimal:.2f} ج.م")

        return amount


class PurchaseFilterForm(forms.Form):
    """Form for filtering purchase orders"""
    
    STATUS_CHOICES = [
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('ordered', 'Ordered'),
        ('partial_received', 'Partially Received'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
        ('returned', 'Returned'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('', 'All Payment Status'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
        ('overdue', 'Overdue'),
    ]
    
    DATE_RANGE_CHOICES = [
        ('', 'All Time'),
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('quarter', 'This Quarter'),
        ('year', 'This Year'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search purchase number, supplier, reference...'
        })
    )
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True),
        required=False,
        empty_label='All Suppliers',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    payment_status = forms.ChoiceField(
        choices=PAYMENT_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_range = forms.ChoiceField(
        choices=DATE_RANGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )


class QuickPurchaseForm(forms.Form):
    """Simplified form for quick purchase orders"""
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    products = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Purchase notes'
        })
    )
    
    payment_due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    def clean_products(self):
        products_data = self.cleaned_data.get('products')
        if not products_data:
            raise ValidationError("At least one product must be selected.")
        
        try:
            import json
            products = json.loads(products_data)
            if not products or len(products) == 0:
                raise ValidationError("At least one product must be selected.")
            
            for product in products:
                if not all(key in product for key in ['product_id', 'quantity', 'unit_cost']):
                    raise ValidationError("Invalid product data.")
                
                if product['quantity'] <= 0:
                    raise ValidationError("Product quantities must be greater than 0.")
                    
                if product['unit_cost'] < 0:
                    raise ValidationError("Product costs cannot be negative.")
            
            return products
        except (json.JSONDecodeError, KeyError, TypeError):
            raise ValidationError("Invalid product data format.")