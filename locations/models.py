from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Emirate(models.Model):
    """
    Model for Emirates (Dubai, Sharjah, Ajman, etc.)
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=120, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('emirate')
        verbose_name_plural = _('emirates')
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PickupLocation(models.Model):
    """
    Model for pickup locations within each emirate
    """
    emirate = models.ForeignKey(Emirate, on_delete=models.CASCADE, related_name='pickup_locations', verbose_name=_('emirate'))
    name = models.CharField(_('name'), max_length=200)
    address = models.TextField(_('address'), blank=True)
    landmark = models.CharField(_('landmark'), max_length=200, blank=True)
    google_maps_link = models.URLField(_('Google Maps link'), blank=True)
    latitude = models.DecimalField(_('latitude'), max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(_('longitude'), max_digits=10, decimal_places=7, null=True, blank=True)
    additional_cost = models.DecimalField(_('additional cost'), max_digits=10, decimal_places=2, default=0.00,
                                         help_text=_('Additional cost for pickup from this location'))
    is_active = models.BooleanField(_('active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('pickup location')
        verbose_name_plural = _('pickup locations')
        ordering = ['emirate', 'display_order', 'name']
    
    def __str__(self):
        return f"{self.name}, {self.emirate.name}"
