from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core import serializers
from .models import Property
from .utils import get_all_properties, get_cache_status, get_redis_cache_metrics


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with caching enabled for 15 minutes.
    Uses low-level cache API for queryset caching.
    """
    # Use the utility function that implements low-level caching
    properties = get_all_properties()
    
    # Convert queryset to JSON-serializable format
    properties_data = []
    for property_obj in properties:
        properties_data.append({
            'id': property_obj.id,
            'title': property_obj.title,
            'description': property_obj.description,
            'price': str(property_obj.price),  # Convert Decimal to string for JSON
            'location': property_obj.location,
            'created_at': property_obj.created_at.isoformat(),
        })
    
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data),
        'cached': True,  # Indicator that this response might be cached
    })


def property_list_no_page_cache(request):
    """
    View to return all properties without page-level caching.
    This view demonstrates only the low-level queryset caching.
    """
    # Use the utility function that implements low-level caching
    properties = get_all_properties()
    
    # Convert queryset to JSON-serializable format
    properties_data = []
    for property_obj in properties:
        properties_data.append({
            'id': property_obj.id,
            'title': property_obj.title,
            'description': property_obj.description,
            'price': str(property_obj.price),  # Convert Decimal to string for JSON
            'location': property_obj.location,
            'created_at': property_obj.created_at.isoformat(),
        })
    
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data),
        'queryset_cached': True,  # Indicator that queryset is cached
        'page_cached': False,     # No page-level caching
    })


def cache_status(request):
    """
    View to display the current cache status for properties.
    """
    status = get_cache_status()
    db_count = Property.objects.count()
    
    return JsonResponse({
        'cache_status': status,
        'database_count': db_count,
        'cache_db_sync': status['cached_count'] == db_count if status['is_cached'] else False,
    })


def cache_metrics(request):
    """
    View to display Redis cache metrics including hit/miss ratios.
    """
    metrics = get_redis_cache_metrics()
    cache_status = get_cache_status()
    
    return JsonResponse({
        'redis_metrics': metrics,
        'application_cache_status': cache_status,
        'timestamp': '2025-08-31T10:00:00Z',  # You might want to add actual timestamp
        'recommendations': {
            'efficiency': metrics.get('cache_efficiency', 'Unknown'),
            'suggestion': get_cache_recommendation(metrics.get('hit_ratio_percentage', 0))
        }
    })


def get_cache_recommendation(hit_ratio):
    """
    Get cache optimization recommendations based on hit ratio.
    """
    if hit_ratio >= 90:
        return "Excellent cache performance! Your cache is working optimally."
    elif hit_ratio >= 80:
        return "Good cache performance. Consider monitoring for consistency."
    elif hit_ratio >= 60:
        return "Fair cache performance. Consider increasing cache TTL or reviewing cache keys."
    elif hit_ratio >= 40:
        return "Poor cache performance. Review caching strategy and cache invalidation logic."
    else:
        return "Very poor cache performance. Consider redesigning your caching approach."
