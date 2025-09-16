# Generated manually for unit migration

from django.db import migrations, models
import django.db.models.deletion


def create_initial_units(apps, schema_editor):
    """Create initial units and migrate existing product data"""
    Unit = apps.get_model('inventory', 'Unit')
    Product = apps.get_model('inventory', 'Product')
    
    # Create initial units
    units_data = [
        {'id': 1, 'name': 'piece', 'name_arabic': 'قطعة', 'abbreviation': 'قطع', 'description': 'وحدة العد للقطع الفردية'},
        {'id': 2, 'name': 'set', 'name_arabic': 'طقم', 'abbreviation': 'طقم', 'description': 'مجموعة من القطع المترابطة'},
        {'id': 3, 'name': 'pair', 'name_arabic': 'زوج', 'abbreviation': 'زوج', 'description': 'زوج من القطع المتطابقة'},
        {'id': 4, 'name': 'meter', 'name_arabic': 'متر', 'abbreviation': 'م', 'description': 'وحدة قياس الطول'},
        {'id': 5, 'name': 'liter', 'name_arabic': 'لتر', 'abbreviation': 'لتر', 'description': 'وحدة قياس السوائل'},
        {'id': 6, 'name': 'kilogram', 'name_arabic': 'كيلوجرام', 'abbreviation': 'كجم', 'description': 'وحدة قياس الوزن'},
        {'id': 7, 'name': 'box', 'name_arabic': 'صندوق', 'abbreviation': 'صندوق', 'description': 'وحدة التعبئة في صناديق'},
    ]
    
    for unit_data in units_data:
        Unit.objects.create(**unit_data, is_active=True)


def reverse_create_initial_units(apps, schema_editor):
    """Remove all units"""
    Unit = apps.get_model('inventory', 'Unit')
    Unit.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_category_options_alter_customer_options_and_more'),
    ]

    operations = [
        # Create Unit model
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='اسم الوحدة')),
                ('name_arabic', models.CharField(max_length=50, verbose_name='الاسم بالعربية')),
                ('abbreviation', models.CharField(max_length=10, verbose_name='الاختصار')),
                ('description', models.TextField(blank=True, verbose_name='الوصف')),
                ('is_active', models.BooleanField(default=True, verbose_name='نشط')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'وحدة قياس',
                'verbose_name_plural': 'وحدات القياس',
                'db_table': 'units',
                'ordering': ['name_arabic'],
            },
        ),
        
        # Update Brand model options
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['name'], 'verbose_name': 'علامة تجارية', 'verbose_name_plural': 'العلامات التجارية'},
        ),
        
        # Create initial units
        migrations.RunPython(create_initial_units, reverse_create_initial_units),
        
        # Add temporary unit_temp field to Product
        migrations.AddField(
            model_name='product',
            name='unit_temp',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='products_temp', to='inventory.unit'),
        ),
    ]
