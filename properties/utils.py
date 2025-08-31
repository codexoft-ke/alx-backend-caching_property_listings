from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Get all properties from cache or database.
    Uses low-level cache API to cache the queryset for 1 hour.
    
    Returns:
        QuerySet: All Property objects
    """
    # Try to get properties from cache first
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        print("Properties retrieved from cache")  # Debug info
        return cached_properties
    
    # If not in cache, fetch from database
    print("Properties fetched from database")  # Debug info
    queryset = Property.objects.all()
    
    # Convert queryset to list to make it cacheable
    properties_list = list(queryset)
    
    # Store in cache for 1 hour (3600 seconds)
    cache.set('all_properties', properties_list, 3600)
    
    return properties_list


def invalidate_properties_cache():
    """
    Utility function to invalidate the properties cache.
    Useful when properties are added, updated, or deleted.
    """
    cache.delete('all_properties')
    print("Properties cache invalidated")  # Debug info


def get_cache_status():
    """
    Utility function to check if properties are cached.
    
    Returns:
        dict: Cache status information
    """
    cached_properties = cache.get('all_properties')
    return {
        'is_cached': cached_properties is not None,
        'cached_count': len(cached_properties) if cached_properties else 0,
        'cache_key': 'all_properties'
    }
