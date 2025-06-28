from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('api/emirates/', views.get_emirates, name='api_emirates'),
    path('api/pickup-locations/', views.get_pickup_locations, name='api_pickup_locations'),
    path('api/pickup-locations/<int:emirate_id>/', views.get_pickup_locations, name='api_pickup_locations_by_emirate'),
]
