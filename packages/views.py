from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import (
    Package, PackageCategory, PackageReview,
    PackageInclusion, PackageAddon
)
from .forms import PackageReviewForm


class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Package.objects.filter(is_active=True)
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Filter by transportation type if provided
        transportation = self.request.GET.get('transportation')
        if transportation:
            queryset = queryset.filter(transportation_type=transportation)
            
        # Sort by price if requested
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'duration_asc':
            queryset = queryset.order_by('duration_hours')
        elif sort == 'duration_desc':
            queryset = queryset.order_by('-duration_hours')
        else:
            # Default sorting: featured packages first, then by name
            queryset = queryset.order_by('-is_featured', 'name')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories to context
        context['categories'] = PackageCategory.objects.filter(is_active=True)
        
        # Add active category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(PackageCategory, slug=category_slug, is_active=True)
        
        # Add current transportation filter
        context['current_transportation'] = self.request.GET.get('transportation', '')
        
        # Add current sort option
        context['current_sort'] = self.request.GET.get('sort', '')
        
        # Add all packages for the infinite scroll animation
        context['all_packages'] = Package.objects.filter(is_active=True).order_by('-is_featured', 'name')
        
        return context


class PackageDetailView(DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'
    slug_url_kwarg = 'package_slug'
    
    def get_queryset(self):
        return Package.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = self.get_object()
        
        # Get related packages (same category)
        context['related_packages'] = Package.objects.filter(
            category=package.category, 
            is_active=True
        ).exclude(id=package.id)[:4]
        
        # Get approved reviews for this package
        context['reviews'] = package.reviews.filter(is_approved=True).order_by('-created_at')
        
        # Add review form for logged-in users
        context['review_form'] = PackageReviewForm()
        
        return context


class PackageReviewCreateView(CreateView):
    model = PackageReview
    form_class = PackageReviewForm
    template_name = 'packages/package_detail.html'  # Fallback template, though we'll redirect
    
    def form_valid(self, form):
        # Set package ID from URL parameter
        form.instance.package_id = self.kwargs.get('package_id')
        
        # If user is authenticated, associate the review with their account
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        # For anonymous users, use the name and email from the form
        else:
            form.instance.name = form.cleaned_data.get('name', 'Anonymous')
            form.instance.email = form.cleaned_data.get('email', '')
        
        # Save the form
        self.object = form.save()
        
        # Debug message to confirm review was saved
        print(f"Review saved to database: ID={self.object.id}, Title={self.object.title}, Rating={self.object.rating}")
        
        # Add success message
        messages.success(self.request, _('Your review has been submitted and is pending approval.'))
        
        # Redirect back to the package detail page
        return redirect('package_detail', package_slug=self.object.package.slug)
    
    def form_invalid(self, form):
        # If form is invalid, redirect back to package detail page with error message
        package_id = self.kwargs.get('package_id')
        package = get_object_or_404(Package, id=package_id)
        messages.error(self.request, _('There was an error with your review submission. Please try again.'))
        return redirect('package_detail', package_slug=package.slug)
