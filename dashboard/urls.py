from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('bookings/', views.booking_list, name='dashboard_booking_list'),
    path('bookings/<str:booking_id>/', views.booking_detail, name='dashboard_booking_detail'),
    path('bookings/<str:booking_id>/update-status/', views.update_booking_status, name='dashboard_update_booking_status'),
    path('packages/', views.package_list, name='dashboard_package_list'),
    path('users/', views.user_list, name='dashboard_user_list'),
    path('reviews/', views.review_list, name='dashboard_review_list'),
    path('reviews/toggle-approval/<int:review_id>/', views.toggle_review_approval, name='dashboard_toggle_review_approval'),
]
