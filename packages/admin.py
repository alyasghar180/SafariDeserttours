from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    PackageCategory, Package, PackageImage, PackageInclusion, 
    PackageInclusionRelation, PackageAddon, PackageAddonRelation, PackageReview
)

@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'icon', 'is_active')
        }),
    )


class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1
    fields = ('image', 'title', 'alt_text', 'display_order', 'is_active')


class PackageInclusionRelationInline(admin.TabularInline):
    model = PackageInclusionRelation
    extra = 1
    verbose_name = _('Inclusion')
    verbose_name_plural = _('Inclusions')


class PackageAddonRelationInline(admin.TabularInline):
    model = PackageAddonRelation
    extra = 1
    fields = ('addon', 'special_price')
    verbose_name = _('Addon')
    verbose_name_plural = _('Addons')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'transportation_type', 'price', 'is_featured', 'is_active')
    list_filter = ('category', 'transportation_type', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PackageImageInline, PackageInclusionRelationInline, PackageAddonRelationInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'short_description', 'featured_image')
        }),
        (_('Pricing'), {
            'fields': ('price', 'child_price')
        }),
        (_('Transportation'), {
            'fields': ('transportation_type', 'duration_hours', 'pickup_time_start', 'pickup_time_end', 'dropoff_time_start', 'dropoff_time_end')
        }),
        (_('Display Options'), {
            'fields': ('is_featured', 'is_active')
        }),
    )


@admin.register(PackageInclusion)
class PackageInclusionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    list_editable = ('display_order', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon', 'display_order', 'is_active')
        }),
    )


@admin.register(PackageAddon)
class PackageAddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_per_person', 'display_order', 'is_active')
    list_filter = ('is_active', 'is_per_person')
    search_fields = ('name', 'description')
    list_editable = ('display_order', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'is_per_person')
        }),
        (_('Display Options'), {
            'fields': ('icon', 'image', 'display_order', 'is_active')
        }),
    )


@admin.register(PackageReview)
class PackageReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'get_reviewer', 'rating', 'title', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('title', 'comment', 'name', 'email', 'user__username', 'user__email', 'package__name')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'package')
    fieldsets = (
        (None, {
            'fields': ('package', 'user', 'name', 'email')
        }),
        (_('Review'), {
            'fields': ('rating', 'title', 'comment')
        }),
        (_('Moderation'), {
            'fields': ('is_approved', 'created_at', 'updated_at')
        }),
    )
    
    def get_reviewer(self, obj):
        if obj.user:
            return obj.user.username
        return obj.name
    get_reviewer.short_description = _('Reviewer')
