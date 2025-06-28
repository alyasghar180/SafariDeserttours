from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.sms_test_dashboard, name='sms_test_dashboard'),
    path('test/send/', views.send_test_sms, name='send_test_sms'),
    path('test/booking/', views.test_booking_sms, name='test_booking_sms'),
    path('config/update/', views.update_sms_config, name='update_sms_config'),
]
