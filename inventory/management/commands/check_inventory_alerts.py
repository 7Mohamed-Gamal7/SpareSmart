from django.core.management.base import BaseCommand
from django.utils import timezone
from inventory.models import Product, InventoryAlert
from django.db.models import Q


class Command(BaseCommand):
    help = 'Check inventory levels and generate alerts for low stock, out of stock, and reorder requirements'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-resolved',
            action='store_true',
            help='Clear resolved alerts older than 30 days',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regenerate all alerts',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting inventory alerts check...'))
        
        if options['clear_resolved']:
            self.clear_old_resolved_alerts()
        
        if options['force']:
            # Clear all existing active alerts to regenerate
            InventoryAlert.objects.filter(status='active').delete()
            self.stdout.write(self.style.WARNING('Cleared all active alerts for regeneration'))
        
        # Get all active products
        products = Product.objects.filter(is_active=True)
        alerts_created = 0
        alerts_updated = 0
        
        for product in products:
            alerts_for_product = self.check_product_alerts(product)
            alerts_created += alerts_for_product['created']
            alerts_updated += alerts_for_product['updated']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Inventory alerts check completed. '
                f'Created: {alerts_created}, Updated: {alerts_updated}'
            )
        )

    def check_product_alerts(self, product):
        """Check and create/update alerts for a specific product"""
        alerts_created = 0
        alerts_updated = 0
        
        # Check for out of stock
        if product.current_stock <= 0:
            alert, created = self.create_or_update_alert(
                product=product,
                alert_type='out_of_stock',
                message=f'{product.name} is out of stock',
                recommended_action=f'Urgent: Reorder {product.name} immediately. Current stock: {product.current_stock}'
            )
            if created:
                alerts_created += 1
            else:
                alerts_updated += 1
        
        # Check for low stock (at or below reorder level)
        elif product.current_stock <= product.reorder_level:
            if product.current_stock <= product.minimum_stock:
                alert_type = 'low_stock'
                priority = 'High'
                message = f'{product.name} has critically low stock'
            else:
                alert_type = 'reorder'
                priority = 'Medium'
                message = f'{product.name} has reached reorder level'
            
            recommended_quantity = max(
                product.maximum_stock - product.current_stock,
                product.reorder_level * 2
            )
            
            alert, created = self.create_or_update_alert(
                product=product,
                alert_type=alert_type,
                message=message,
                recommended_action=f'{priority} Priority: Reorder {recommended_quantity} units of {product.name}. '
                                  f'Current stock: {product.current_stock}, Minimum: {product.minimum_stock}, '
                                  f'Reorder level: {product.reorder_level}'
            )
            if created:
                alerts_created += 1
            else:
                alerts_updated += 1
        
        # Check for overstock
        elif product.current_stock > product.maximum_stock:
            alert, created = self.create_or_update_alert(
                product=product,
                alert_type='overstock',
                message=f'{product.name} is overstocked',
                recommended_action=f'Consider promotions or discounts for {product.name}. '
                                  f'Current stock: {product.current_stock}, Maximum: {product.maximum_stock}'
            )
            if created:
                alerts_created += 1
            else:
                alerts_updated += 1
        
        else:
            # Product stock is normal, resolve any existing alerts
            self.resolve_product_alerts(product)
        
        return {'created': alerts_created, 'updated': alerts_updated}

    def create_or_update_alert(self, product, alert_type, message, recommended_action):
        """Create new alert or update existing one"""
        existing_alert = InventoryAlert.objects.filter(
            product=product,
            alert_type=alert_type,
            status='active'
        ).first()
        
        if existing_alert:
            # Update existing alert
            existing_alert.message = message
            existing_alert.current_stock = product.current_stock
            existing_alert.recommended_action = recommended_action
            existing_alert.save()
            return existing_alert, False
        else:
            # Create new alert
            new_alert = InventoryAlert.objects.create(
                product=product,
                alert_type=alert_type,
                message=message,
                current_stock=product.current_stock,
                recommended_action=recommended_action,
                status='active'
            )
            return new_alert, True

    def resolve_product_alerts(self, product):
        """Resolve all active alerts for a product when stock is normal"""
        InventoryAlert.objects.filter(
            product=product,
            status='active'
        ).update(status='resolved')

    def clear_old_resolved_alerts(self):
        """Clear resolved alerts older than 30 days"""
        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        deleted_count = InventoryAlert.objects.filter(
            status='resolved',
            acknowledged_at__lt=thirty_days_ago
        ).delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(f'Cleared {deleted_count} old resolved alerts')
        )