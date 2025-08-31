from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core import serializers
from .models import Property
from .utils import get_all_properties


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
