# Generated manually

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_booking_cancellation_reason_booking_cancelled_at'),
        ('locations', '0001_initial'),
    ]

    operations = [
        # First add the text field for pickup_location_text
        migrations.AddField(
            model_name='booking',
            name='pickup_location_text',
            field=models.CharField(blank=True, help_text='Manual entry of pickup location if not selecting from predefined locations', max_length=255, verbose_name='pickup location text'),
        ),
        # Add address_details field
        migrations.AddField(
            model_name='booking',
            name='address_details',
            field=models.TextField(blank=True, help_text='Additional address details for pickup', verbose_name='address details'),
        ),
        # Add emirate field with null=True to avoid integrity errors
        migrations.AddField(
            model_name='booking',
            name='emirate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='locations.emirate', verbose_name='emirate'),
        ),
        # Modify pickup_location field to be a ForeignKey to PickupLocation
        migrations.AlterField(
            model_name='booking',
            name='pickup_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='locations.pickuplocation', verbose_name='pickup location'),
        ),
    ]
