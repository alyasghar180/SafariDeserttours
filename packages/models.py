from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.exceptions import ValidationError

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


class PackageInclusion(models.Model):
    """
    Model for activities and amenities included in packages.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    icon = models.CharField(_('icon class'), max_length=50, blank=True, help_text=_('Font Awesome icon class (e.g., fa-utensils)'))
    is_active = models.BooleanField(_('active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package inclusion')
        verbose_name_plural = _('package inclusions')
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class PackageInclusionRelation(models.Model):
    """
    Relation model connecting packages with their inclusions.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='inclusion_relations', verbose_name=_('package'))
    inclusion = models.ForeignKey(PackageInclusion, on_delete=models.CASCADE, related_name='package_relations', verbose_name=_('inclusion'))
    
    class Meta:
        verbose_name = _('package inclusion relation')
        verbose_name_plural = _('package inclusion relations')
        unique_together = ('package', 'inclusion')
    
    def __str__(self):
        return f"{self.package.name} - {self.inclusion.name}"


class PackageAddon(models.Model):
    """
    Model for optional add-ons that can be purchased with packages.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    is_per_person = models.BooleanField(_('per person'), default=True, help_text=_('If checked, price is per person. Otherwise, price is per booking.'))
    icon = models.CharField(_('icon class'), max_length=50, blank=True, help_text=_('Font Awesome icon class (e.g., fa-motorcycle)'))
    image = models.ImageField(_('image'), upload_to='addons/', blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    display_order = models.PositiveIntegerField(_('display order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package addon')
        verbose_name_plural = _('package addons')
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name


class PackageAddonRelation(models.Model):
    """
    Relation model connecting packages with their available add-ons.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='addon_relations', verbose_name=_('package'))
    addon = models.ForeignKey(PackageAddon, on_delete=models.CASCADE, related_name='package_relations', verbose_name=_('addon'))
    special_price = models.DecimalField(_('special price'), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_('Special price for this addon when purchased with this package. Leave blank to use the default addon price.'))
    
    class Meta:
        verbose_name = _('package addon relation')
        verbose_name_plural = _('package addon relations')
        unique_together = ('package', 'addon')
    
    def __str__(self):
        return f"{self.package.name} - {self.addon.name}"
    
    def get_price(self):
        """Returns the special price if set, otherwise the default addon price."""
        return self.special_price if self.special_price is not None else self.addon.price


class PackageReview(models.Model):
    """
    Model for customer reviews of packages.
    """
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('package'))
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='package_reviews', verbose_name=_('user'), null=True, blank=True)
    name = models.CharField(_('name'), max_length=100, blank=True, help_text=_('Name of the reviewer if not a registered user'))
    email = models.EmailField(_('email'), blank=True, help_text=_('Email of the reviewer if not a registered user'))
    rating = models.PositiveSmallIntegerField(_('rating'), choices=RATING_CHOICES)
    title = models.CharField(_('title'), max_length=100)
    comment = models.TextField(_('comment'))
    is_approved = models.BooleanField(_('approved'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('package review')
        verbose_name_plural = _('package reviews')
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"{self.package.name} - {self.user.username} - {self.rating}/5"
        return f"{self.package.name} - {self.name} - {self.rating}/5"
    
    def clean(self):
        # Either user or name/email should be provided
        if not self.user and not self.name:
            raise ValidationError(_('Either a user or a name must be provided.'))

