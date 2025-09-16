# Generated manually for finalizing unit migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_migrate_product_units'),
    ]

    operations = [
        # Remove old unit field
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        
        # Rename unit_temp to unit
        migrations.RenameField(
            model_name='product',
            old_name='unit_temp',
            new_name='unit',
        ),
        
        # Make unit field required (not null)
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='inventory.unit'),
        ),
    ]
