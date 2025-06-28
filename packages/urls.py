from django.urls import path
from . import views

urlpatterns = [
    # Package list views
    path('', views.PackageListView.as_view(), name='package_list'),
    path('category/<slug:category_slug>/', views.PackageListView.as_view(), name='package_list_by_category'),
    
    # Package detail view
    path('<slug:package_slug>/', views.PackageDetailView.as_view(), name='package_detail'),
    
    # Package review
    path('review/<int:package_id>/add/', views.PackageReviewCreateView.as_view(), name='add_package_review'),
]
