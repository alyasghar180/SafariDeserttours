from django.urls import path
from . import views

urlpatterns = [
    # Booking creation and confirmation
    path('package/<slug:package_slug>/book/', views.BookingCreateView.as_view(), name='create_booking'),
    path('confirmation/', views.BookingConfirmationView.as_view(), name='booking_confirmation'),
    
    # Booking details and history
    path('detail/<str:booking_id>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('history/', views.BookingHistoryView.as_view(), name='booking_history'),
    
    # Booking management
    path('cancel/<str:booking_id>/', views.BookingCancelView.as_view(), name='booking_cancel'),
    path('update/<str:booking_id>/', views.BookingUpdateView.as_view(), name='booking_update'),
]
