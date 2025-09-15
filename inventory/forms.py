from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, Brand, Customer, Supplier, StockMovement
import re

class ProductForm(forms.ModelForm):
    """Form for creating and updating products"""
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'sku', 'barcode', 'category', 'brand', 'unit',
            'cost_price', 'selling_price', 'wholesale_price', 'current_stock',
            'minimum_stock', 'maximum_stock', 'reorder_level', 'weight', 'Dimensions',
            'color', 'materials', 'image', 'datasheet', 'compatible_vehicles',
            'part_number', 'oem_number', 'is_active', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Description'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SKU'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Barcode'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'wholesale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'current_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'minimum_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'maximum_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'Dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'L x W x H'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'materials': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'materials'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'datasheet': forms.FileInput(attrs={'class': 'form-control-file'}),
            'compatible_vehicles': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'المركبات المتوافقة'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم القطعة'}),
            'oem_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'رقم الشركة المصنعة للمعدات الأصلية'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if sku:
            # Check for duplicate SKU
            query = Product.objects.filter(sku=sku)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Product with this SKU already exists.")
        return sku

    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        if barcode:
            # Check for duplicate barcode
            query = Product.objects.filter(barcode=barcode)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Product with this barcode already exists.")
        return barcode

    def clean(self):
        cleaned_data = super().clean()
        cost_price = cleaned_data.get('cost_price')
        selling_price = cleaned_data.get('selling_price')
        wholesale_price = cleaned_data.get('wholesale_price')
        minimum_stock = cleaned_data.get('minimum_stock')
        maximum_stock = cleaned_data.get('maximum_stock')
        reorder_level = cleaned_data.get('reorder_level')

        # Validate pricing
        if cost_price and selling_price:
            if selling_price <= cost_price:
                raise ValidationError("Selling price must be greater than cost price.")

        if wholesale_price and cost_price:
            if wholesale_price <= cost_price:
                raise ValidationError("Wholesale price must be greater than cost price.")

        # Validate stock levels
        if minimum_stock and maximum_stock:
            if minimum_stock >= maximum_stock:
                raise ValidationError("Maximum stock must be greater than minimum stock.")

        if reorder_level and minimum_stock:
            if reorder_level < minimum_stock:
                raise ValidationError("إعادة ترتيب المستوى should not be less than minimum stock.")

        return cleaned_data

class CategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'vehicle_type', 'parent_category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Category Description'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'parent_category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            query = Category.objects.filter(name=name)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Category with this name already exists.")
        return name

class BrandForm(forms.ModelForm):
    """Form for creating and updating brands"""
    
    class Meta:
        model = Brand
        fields = ['name', 'description', 'logo', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brand Description'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            query = Brand.objects.filter(name=name)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise ValidationError("Brand with this name already exists.")
        return name

class CustomerForm(forms.ModelForm):
    """Form for creating and updating customers"""
    
    class Meta:
        model = Customer
        fields = [
            'name', 'customer_type', 'email', 'phone', 'address', 'city',
            'tax_number', 'credit_limit', 'discount_percentage', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax Number'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SupplierForm(forms.ModelForm):
    """Form for creating and updating suppliers"""
    
    class Meta:
        model = Supplier
        fields = [
            'name', 'contact_person', 'email', 'phone', 'address', 'city',
            'tax_number', 'payment_terms', 'credit_limit', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tax Number'}),
            'payment_terms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Payment Terms'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class StockAdjustmentForm(forms.ModelForm):
    """Form for stock adjustments"""
    
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'unit_cost', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adjustment notes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter movement types for adjustments
        self.fields['movement_type'].choices = [
            ('adjustment', 'Stock Adjustment'),
            ('damaged', 'Damaged'),
            ('lost', 'Lost'),
        ]

class ProductFilterForm(forms.Form):
    """Form for filtering products"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.filter(is_active=True),
        required=False,
        empty_label="All Brands",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    vehicle_type = forms.ChoiceField(
        choices=[('', 'All Vehicle Types')] + Category.VEHICLE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    stock_status = forms.ChoiceField(
        choices=[
            ('', 'All Stock Status'),
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    is_active = forms.ChoiceField(
        choices=[
            ('', 'All Products'),
            ('1', 'Active Only'),
            ('0', 'Inactive Only'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class BulkActionForm(forms.Form):
    """Form for bulk actions on products"""
    
    ACTION_CHOICES = [
        ('activate', 'Activate'),
        ('deactivate', 'Deactivate'),
        ('delete', 'Delete'),
        ('update_category', 'Update Category'),
        ('update_brand', 'Update Brand'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    selected_products = forms.CharField(
        widget=forms.HiddenInput()
    )
    
    # Optional fields for updates
    new_category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    new_brand = forms.ModelChoiceField(
        queryset=Brand.objects.filter(is_active=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )