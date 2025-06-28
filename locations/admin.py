from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Emirate, PickupLocation


class PickupLocationInline(admin.TabularInline):
    model = PickupLocation
    extra = 1


@admin.register(Emirate)
class EmirateAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PickupLocationInline]
    list_editable = ('display_order', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Settings'), {
            'fields': ('display_order', 'is_active')
        }),
    )


@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'emirate', 'additional_cost', 'display_order', 'is_active')
    list_filter = ('emirate', 'is_active')
    search_fields = ('name', 'address', 'landmark')
    list_editable = ('display_order', 'is_active', 'additional_cost')
    fieldsets = (
        (None, {
            'fields': ('emirate', 'name', 'address', 'landmark')
        }),
        (_('Map Information'), {
            'fields': ('google_maps_link', 'latitude', 'longitude')
        }),
        (_('Settings'), {
            'fields': ('additional_cost', 'display_order', 'is_active')
        }),
    )
