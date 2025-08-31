#!/usr/bin/env python
"""
Test script to demonstrate Redis cache metrics functionality.
Run this script to test the cache metrics analysis.
"""

import os
import sys
import django
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_caching_property_listings.settings')
django.setup()

from properties.models import Property
from properties.utils import get_redis_cache_metrics, get_all_properties, reset_redis_stats, get_cache_status


def main():
    print("=== Redis Cache Metrics Analysis Test ===\n")
    
    # 1. Reset Redis stats for clean testing (optional)
    print("1. Resetting Redis statistics...")
    reset_redis_stats()
    
    # 2. Clear existing data and cache
    print("\n2. Clearing existing data...")
    Property.objects.all().delete()
    
    # 3. Create test data
    print("\n3. Creating test properties...")
    test_properties = [
        {
            'title': 'Oceanview Villa',
            'description': 'Luxury villa with stunning ocean views',
            'price': Decimal('1200000.00'),
            'location': 'Malibu, CA'
        },
        {
            'title': 'Downtown Loft',
            'description': 'Modern loft in the heart of downtown',
            'price': Decimal('750000.00'),
            'location': 'New York, NY'
        },
        {
            'title': 'Mountain Retreat',
            'description': 'Peaceful cabin in the mountains',
            'price': Decimal('450000.00'),
            'location': 'Aspen, CO'
        },
        {
            'title': 'Beachfront Condo',
            'description': 'Luxury condo steps from the beach',
            'price': Decimal('850000.00'),
            'location': 'Miami, FL'
        },
        {
            'title': 'Suburban Home',
            'description': 'Family-friendly home in quiet neighborhood',
            'price': Decimal('325000.00'),
            'location': 'Austin, TX'
        }
    ]
    
    for prop_data in test_properties:
        Property.objects.create(**prop_data)
    
    print(f"Created {len(test_properties)} test properties")
    
    # 4. Get initial metrics
    print("\n4. Initial Redis metrics:")
    initial_metrics = get_redis_cache_metrics()
    
    # 5. Generate cache hits and misses
    print("\n5. Generating cache operations...")
    
    # First call - should be a cache miss
    print("  - First call (cache miss):")
    properties1 = get_all_properties()
    print(f"    Retrieved {len(properties1)} properties")
    
    # Second call - should be a cache hit
    print("  - Second call (cache hit):")
    properties2 = get_all_properties()
    print(f"    Retrieved {len(properties2)} properties")
    
    # Third call - should be another cache hit
    print("  - Third call (cache hit):")
    properties3 = get_all_properties()
    print(f"    Retrieved {len(properties3)} properties")
    
    # 6. Get final metrics
    print("\n6. Final Redis metrics after operations:")
    final_metrics = get_redis_cache_metrics()
    
    # 7. Show cache status
    print("\n7. Current cache status:")
    cache_status = get_cache_status()
    print(f"   Cache Status: {cache_status}")
    
    # 8. Summary
    print("\n8. Summary:")
    print(f"   - Properties in database: {Property.objects.count()}")
    print(f"   - Properties in cache: {cache_status['cached_count']}")
    print(f"   - Cache hit ratio: {final_metrics.get('hit_ratio_percentage', 0)}%")
    print(f"   - Cache efficiency: {final_metrics.get('cache_efficiency', 'Unknown')}")
    
    print("\n=== Test completed successfully! ===")


if __name__ == "__main__":
    main()
