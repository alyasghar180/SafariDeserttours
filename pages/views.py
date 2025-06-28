from django.shortcuts import render
from packages.models import Package, PackageCategory, PackageImage

def home(request):
    """
    View for the home page.
    Displays featured packages and package categories.
    """    # Get featured packages
    featured_packages = Package.objects.filter(is_featured=True, is_active=True)[:6]
    
    # Get all active packages for the scroll animation
    all_packages = Package.objects.filter(is_active=True)
    
    # Get all active categories
    categories = PackageCategory.objects.filter(is_active=True)
    
    context = {
        'featured_packages': featured_packages,
        'all_packages': all_packages,
        'categories': categories,
    }
    
    return render(request, 'pages/home.html', context)

def about(request):
    """
    View for the about page.
    """
    return render(request, 'pages/about.html')

def contact(request):
    """
    View for the contact page.
    """
    return render(request, 'pages/contact.html')

def gallery(request):
    """
    View for the gallery page.
    Displays images from packages.
    """
    # Get all active package images
    package_images = PackageImage.objects.filter(is_active=True).order_by('?')[:12]
    
    context = {
        'package_images': package_images,
    }
    
    return render(request, 'pages/gallery.html', context)
