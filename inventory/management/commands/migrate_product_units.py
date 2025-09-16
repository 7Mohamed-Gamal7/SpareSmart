from django.core.management.base import BaseCommand
from django.db import transaction
from inventory.models import Product, Unit

class Command(BaseCommand):
    help = 'Migrate existing product units from choices to Unit model'

    def handle(self, *args, **options):
        # Mapping from old unit choices to new Unit IDs
        unit_mapping = {
            'piece': 1,
            'set': 2,
            'pair': 3,
            'meter': 4,
            'liter': 5,
            'kg': 6,
            'box': 7,
        }
        
        with transaction.atomic():
            # Get all products that need migration
            products = Product.objects.all()
            updated_count = 0
            
            for product in products:
                # Get the old unit value (if it exists as a string)
                old_unit = getattr(product, 'unit', None)
                
                if old_unit and isinstance(old_unit, str):
                    # Map to new Unit ID
                    new_unit_id = unit_mapping.get(old_unit, 1)  # Default to 'piece'
                    
                    try:
                        new_unit = Unit.objects.get(id=new_unit_id)
                        # Update the product with the new Unit object
                        Product.objects.filter(id=product.id).update(unit=new_unit)
                        updated_count += 1
                        self.stdout.write(
                            f'Updated product {product.name}: {old_unit} -> {new_unit.name_arabic}'
                        )
                    except Unit.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Unit with ID {new_unit_id} not found for product {product.name}')
                        )
                elif not old_unit:
                    # Set default unit for products without unit
                    try:
                        default_unit = Unit.objects.get(id=1)  # 'piece'
                        Product.objects.filter(id=product.id).update(unit=default_unit)
                        updated_count += 1
                        self.stdout.write(
                            f'Set default unit for product {product.name}: -> {default_unit.name_arabic}'
                        )
                    except Unit.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR('Default unit (piece) not found!')
                        )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} products')
            )
