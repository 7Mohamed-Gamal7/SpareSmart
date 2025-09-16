# Generated manually for unit data migration

from django.db import migrations


def migrate_product_units(apps, schema_editor):
    """Migrate existing product units from string choices to Unit foreign keys"""
    Product = apps.get_model('inventory', 'Product')
    Unit = apps.get_model('inventory', 'Unit')
    
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
    
    # Update all products
    for product in Product.objects.all():
        old_unit = product.unit
        
        # Map old unit to new Unit object
        if old_unit in unit_mapping:
            unit_id = unit_mapping[old_unit]
        else:
            unit_id = 1  # Default to 'piece'
        
        try:
            unit_obj = Unit.objects.get(id=unit_id)
            product.unit_temp = unit_obj
            product.save()
        except Unit.DoesNotExist:
            # Fallback to first available unit
            unit_obj = Unit.objects.first()
            if unit_obj:
                product.unit_temp = unit_obj
                product.save()


def reverse_migrate_product_units(apps, schema_editor):
    """Reverse migration - set unit_temp to None"""
    Product = apps.get_model('inventory', 'Product')
    Product.objects.all().update(unit_temp=None)


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_add_unit_model'),
    ]

    operations = [
        # Migrate data from old unit field to new unit_temp field
        migrations.RunPython(migrate_product_units, reverse_migrate_product_units),
    ]
