from django.core.management.base import BaseCommand
from properties.utils import get_redis_cache_metrics, get_all_properties, reset_redis_stats
from properties.models import Property
from decimal import Decimal
import time


class Command(BaseCommand):
    help = 'Test Redis cache metrics functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-stats',
            action='store_true',
            help='Reset Redis statistics before running the test',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Testing Redis cache metrics...'))
        
        if options['reset_stats']:
            self.stdout.write("Resetting Redis statistics...")
            reset_redis_stats()
            time.sleep(1)
        
        # Display initial metrics
        self.stdout.write("\n=== Initial Cache Metrics ===")
        initial_metrics = get_redis_cache_metrics()
        
        # Clear existing properties and create test data
        self.stdout.write("\nCreating test data...")
        Property.objects.all().delete()
        
        # Create some test properties
        test_properties = [
            {
                'title': 'Luxury Villa',
                'description': 'Beautiful luxury villa with pool',
                'price': Decimal('750000.00'),
                'location': 'Beverly Hills, CA'
            },
            {
                'title': 'Downtown Loft',
                'description': 'Modern loft in city center',
                'price': Decimal('450000.00'),
                'location': 'Manhattan, NY'
            },
            {
                'title': 'Beach Cottage',
                'description': 'Cozy cottage near the beach',
                'price': Decimal('350000.00'),
                'location': 'Malibu, CA'
            }
        ]
        
        for prop_data in test_properties:
            Property.objects.create(**prop_data)
        
        self.stdout.write(f"Created {len(test_properties)} test properties")
        
        # Simulate cache operations to generate metrics
        self.stdout.write("\nSimulating cache operations...")
        
        # First call - should be a cache miss (fetches from DB)
        self.stdout.write("1. First call (cache miss expected):")
        properties1 = get_all_properties()
        self.stdout.write(f"   Retrieved {len(properties1)} properties")
        
        # Second call - should be a cache hit
        self.stdout.write("2. Second call (cache hit expected):")
        properties2 = get_all_properties()
        self.stdout.write(f"   Retrieved {len(properties2)} properties")
        
        # Third call - another cache hit
        self.stdout.write("3. Third call (cache hit expected):")
        properties3 = get_all_properties()
        self.stdout.write(f"   Retrieved {len(properties3)} properties")
        
        # Display final metrics
        self.stdout.write("\n=== Final Cache Metrics ===")
        final_metrics = get_redis_cache_metrics()
        
        # Calculate the difference
        hits_diff = final_metrics['keyspace_hits'] - initial_metrics['keyspace_hits']
        misses_diff = final_metrics['keyspace_misses'] - initial_metrics['keyspace_misses']
        
        self.stdout.write(f"\nOperations performed during this test:")
        self.stdout.write(f"  - Cache hits: {hits_diff}")
        self.stdout.write(f"  - Cache misses: {misses_diff}")
        
        self.stdout.write(self.style.SUCCESS('\nCache metrics test completed!'))
