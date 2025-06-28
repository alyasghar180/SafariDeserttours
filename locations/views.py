from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Emirate, PickupLocation

def get_emirates(request):
    """
    API view to get all active emirates
    """
    emirates = Emirate.objects.filter(is_active=True).order_by('display_order', 'name')
    data = [{
        'id': emirate.id,
        'name': emirate.name,
        'slug': emirate.slug
    } for emirate in emirates]
    return JsonResponse({'emirates': data})

def get_pickup_locations(request, emirate_id=None):
    """
    API view to get pickup locations for a specific emirate
    """
    if emirate_id:
        emirate = get_object_or_404(Emirate, id=emirate_id, is_active=True)
        locations = PickupLocation.objects.filter(
            emirate=emirate,
            is_active=True
        ).order_by('display_order', 'name')
    else:
        locations = PickupLocation.objects.filter(
            is_active=True
        ).order_by('emirate__display_order', 'emirate__name', 'display_order', 'name')
    
    data = [{
        'id': location.id,
        'name': location.name,
        'emirate': {
            'id': location.emirate.id,
            'name': location.emirate.name
        },
        'additional_cost': float(location.additional_cost)
    } for location in locations]
    
    return JsonResponse({'locations': data})
