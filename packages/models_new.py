from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class PackageCategory(models.Model):
    """
    Model for categorizing packages (e.g., Standard, Premium, Family, etc.)
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=120, unique=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon class'), max_length=50, blank=True, help_text=_('Font Awesome icon class (e.g., fa-car)'))
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package category')
        verbose_name_plural = _('package categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Package(models.Model):
    """
    Model for desert safari packages.
    """
    TRANSPORTATION_CHOICES = (
        ('self_drive', _('Self Drive')),
        ('bus', _('Bus Transportation')),
        ('4x4', _('4x4 Transportation')),
    )
    
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=220, unique=True, blank=True)
    category = models.ForeignKey(PackageCategory, on_delete=models.CASCADE, related_name='packages', verbose_name=_('category'))
    description = models.TextField(_('description'))
    short_description = models.CharField(_('short description'), max_length=255, blank=True)
    transportation_type = models.CharField(_('transportation type'), max_length=20, choices=TRANSPORTATION_CHOICES)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    child_price = models.DecimalField(_('child price'), max_digits=10, decimal_places=2, null=True, blank=True)
    duration_hours = models.DecimalField(_('duration (hours)'), max_digits=4, decimal_places=1)
    pickup_time_start = models.TimeField(_('pickup time start'), null=True, blank=True)
    pickup_time_end = models.TimeField(_('pickup time end'), null=True, blank=True)
    dropoff_time_start = models.TimeField(_('dropoff time start'), null=True, blank=True)
    dropoff_time_end = models.TimeField(_('dropoff time end'), null=True, blank=True)
    featured_image = models.ImageField(_('featured image'), upload_to='packages/', blank=True)
    is_featured = models.BooleanField(_('featured'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PackageImage(models.Model):
    """
    Model for package gallery images.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='images', verbose_name=_('package'))
    image = models.ImageField(_('image'), upload_to='packages/gallery/')
    title = models.CharField(_('title'), max_length=100, blank=True)
    alt_text = models.CharField(_('alt text'), max_length=200, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package image')
        verbose_name_plural = _('package images')
        ordering = ['display_order']
    
    def __str__(self):
        return f"{self.package.name} - Image {self.id}"
