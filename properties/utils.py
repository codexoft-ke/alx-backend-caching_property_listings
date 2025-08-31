from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Set up logging for cache metrics
logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Cache metrics including hits, misses, hit ratio, and other stats
    """
    try:
        # Get Redis connection using django_redis
        redis_client = get_redis_connection("default")
        
        # Get Redis INFO stats
        info = redis_client.info()
        
        # Extract keyspace statistics
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate total operations and hit ratio
        total_operations = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_operations * 100) if total_operations > 0 else 0
        miss_ratio = (keyspace_misses / total_operations * 100) if total_operations > 0 else 0
        
        # Get additional useful metrics
        used_memory = info.get('used_memory', 0)
        used_memory_human = info.get('used_memory_human', 'N/A')
        connected_clients = info.get('connected_clients', 0)
        total_commands_processed = info.get('total_commands_processed', 0)
        
        # Get database-specific information
        db_info = {}
        for key, value in info.items():
            if key.startswith('db'):
                db_info[key] = value
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_operations': total_operations,
            'hit_ratio_percentage': round(hit_ratio, 2),
            'miss_ratio_percentage': round(miss_ratio, 2),
            'used_memory_bytes': used_memory,
            'used_memory_human': used_memory_human,
            'connected_clients': connected_clients,
            'total_commands_processed': total_commands_processed,
            'database_info': db_info,
            'cache_efficiency': 'Good' if hit_ratio > 80 else 'Fair' if hit_ratio > 50 else 'Poor'
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics: "
                   f"Hits: {keyspace_hits}, "
                   f"Misses: {keyspace_misses}, "
                   f"Hit Ratio: {hit_ratio:.2f}%, "
                   f"Memory Used: {used_memory_human}")
        
        # Print metrics for debugging (can be removed in production)
        print(f"=== Redis Cache Metrics ===")
        print(f"Cache Hits: {keyspace_hits}")
        print(f"Cache Misses: {keyspace_misses}")
        print(f"Total Operations: {total_operations}")
        print(f"Hit Ratio: {hit_ratio:.2f}%")
        print(f"Miss Ratio: {miss_ratio:.2f}%")
        print(f"Memory Used: {used_memory_human}")
        print(f"Cache Efficiency: {metrics['cache_efficiency']}")
        print(f"===========================")
        
        return metrics
        
    except Exception as e:
        error_message = f"Error retrieving Redis cache metrics: {str(e)}"
        logger.error(error_message)
        print(error_message)
        
        return {
            'error': error_message,
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_operations': 0,
            'hit_ratio_percentage': 0,
            'miss_ratio_percentage': 0,
            'cache_efficiency': 'Unknown'
        }


def reset_redis_stats():
    """
    Reset Redis statistics for testing purposes.
    WARNING: This will reset all Redis statistics, not just for this application.
    """
    try:
        redis_client = get_redis_connection("default")
        redis_client.config_resetstat()
        logger.info("Redis statistics have been reset")
        print("Redis statistics have been reset")
        return True
    except Exception as e:
        error_message = f"Error resetting Redis stats: {str(e)}"
        logger.error(error_message)
        print(error_message)
        return False
