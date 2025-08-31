from django.core.management.base import BaseCommand
from decimal import Decimal
from properties.models import Property
from properties.utils import get_all_properties, get_cache_status


class Command(BaseCommand):
    help = 'Test signal-based cache invalidation for properties'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing signal-based cache invalidation...'))
        
        # Clear existing properties
        Property.objects.all().delete()
        
        # Check initial cache status
        status = get_cache_status()
        self.stdout.write(f"Initial cache status: {status}")
        
        # Load properties into cache
        self.stdout.write("\n1. Loading properties into cache...")
        properties = get_all_properties()
        self.stdout.write(f"Loaded {len(properties)} properties")
        
        # Check cache status after loading
        status = get_cache_status()
        self.stdout.write(f"Cache status after loading: {status}")
        
        # Create a new property (should trigger cache invalidation)
        self.stdout.write("\n2. Creating a new property (should invalidate cache)...")
        new_property = Property.objects.create(
            title='Signal Test Property',
            description='A property created to test signal-based cache invalidation',
            price=Decimal('300000.00'),
            location='Test City'
        )
        
        # Check cache status after creation
        status = get_cache_status()
        self.stdout.write(f"Cache status after creating property: {status}")
        
        # Load properties again (should fetch from database)
        self.stdout.write("\n3. Loading properties again...")
        properties = get_all_properties()
        self.stdout.write(f"Loaded {len(properties)} properties")
        
        # Update the property (should trigger cache invalidation)
        self.stdout.write("\n4. Updating the property (should invalidate cache)...")
        new_property.title = 'Updated Signal Test Property'
        new_property.save()
        
        # Check cache status after update
        status = get_cache_status()
        self.stdout.write(f"Cache status after updating property: {status}")
        
        # Delete the property (should trigger cache invalidation)
        self.stdout.write("\n5. Deleting the property (should invalidate cache)...")
        new_property.delete()
        
        # Check final cache status
        status = get_cache_status()
        self.stdout.write(f"Final cache status after deletion: {status}")
        
        self.stdout.write(self.style.SUCCESS('\nSignal-based cache invalidation test completed!'))
