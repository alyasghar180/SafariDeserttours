import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

# Import models
from locations.models import Emirate, PickupLocation

# Create Emirates
emiratesData = [
    {
        'name': 'Dubai',
        'description': 'The most populous city in the UAE and a global city and business hub.',
        'is_active': True,
        'display_order': 1,
    },
    {
        'name': 'Abu Dhabi',
        'description': 'The capital and the second most populous city of the UAE.',
        'is_active': True,
        'display_order': 2,
    },
    {
        'name': 'Sharjah',
        'description': 'The third-most populous city in the United Arab Emirates.',
        'is_active': True,
        'display_order': 3,
    },
    {
        'name': 'Ajman',
        'description': 'The smallest emirate of the United Arab Emirates.',
        'is_active': True,
        'display_order': 4,
    },
]

# Create or update Emirates
for data in emiratesData:
    emirate, created = Emirate.objects.update_or_create(
        name=data['name'],
        defaults={
            'description': data['description'],
            'is_active': data['is_active'],
            'display_order': data['display_order'],
        }
    )
    print(f"{'Created' if created else 'Updated'} Emirate: {emirate.name}")

# Create Pickup Locations for Dubai
dubai = Emirate.objects.get(name='Dubai')
dubai_locations = [
    {
        'name': 'Dubai Marina',
        'address': 'Dubai Marina, Dubai, UAE',
        'landmark': 'Near Marina Mall',
        'additional_cost': 0.00,
        'is_active': True,
        'display_order': 1,
    },
    {
        'name': 'Jumeirah Beach Residence (JBR)',
        'address': 'JBR, Dubai, UAE',
        'landmark': 'The Walk',
        'additional_cost': 0.00,
        'is_active': True,
        'display_order': 2,
    },
    {
        'name': 'Downtown Dubai',
        'address': 'Downtown Dubai, Dubai, UAE',
        'landmark': 'Near Burj Khalifa',
        'additional_cost': 0.00,
        'is_active': True,
        'display_order': 3,
    },
    {
        'name': 'Deira',
        'address': 'Deira, Dubai, UAE',
        'landmark': 'Near Gold Souk',
        'additional_cost': 10.00,
        'is_active': True,
        'display_order': 4,
    },
]

# Create Pickup Locations for Abu Dhabi
abu_dhabi = Emirate.objects.get(name='Abu Dhabi')
abu_dhabi_locations = [
    {
        'name': 'Corniche',
        'address': 'Corniche Road, Abu Dhabi, UAE',
        'landmark': 'Near Corniche Beach',
        'additional_cost': 50.00,
        'is_active': True,
        'display_order': 1,
    },
    {
        'name': 'Yas Island',
        'address': 'Yas Island, Abu Dhabi, UAE',
        'landmark': 'Near Ferrari World',
        'additional_cost': 70.00,
        'is_active': True,
        'display_order': 2,
    },
]

# Create Pickup Locations for Sharjah
sharjah = Emirate.objects.get(name='Sharjah')
sharjah_locations = [
    {
        'name': 'Al Majaz',
        'address': 'Al Majaz, Sharjah, UAE',
        'landmark': 'Near Sharjah Fountain',
        'additional_cost': 40.00,
        'is_active': True,
        'display_order': 1,
    },
    {
        'name': 'Al Khan',
        'address': 'Al Khan, Sharjah, UAE',
        'landmark': 'Near Al Khan Beach',
        'additional_cost': 45.00,
        'is_active': True,
        'display_order': 2,
    },
]

# Create Pickup Locations for Ajman
ajman = Emirate.objects.get(name='Ajman')
ajman_locations = [
    {
        'name': 'Ajman Corniche',
        'address': 'Ajman Corniche, Ajman, UAE',
        'landmark': 'Near Ajman Beach',
        'additional_cost': 60.00,
        'is_active': True,
        'display_order': 1,
    },
]

# Create all pickup locations
all_locations = {
    dubai: dubai_locations,
    abu_dhabi: abu_dhabi_locations,
    sharjah: sharjah_locations,
    ajman: ajman_locations,
}

for emirate, locations in all_locations.items():
    for data in locations:
        location, created = PickupLocation.objects.update_or_create(
            emirate=emirate,
            name=data['name'],
            defaults={
                'address': data['address'],
                'landmark': data['landmark'],
                'additional_cost': data['additional_cost'],
                'is_active': data['is_active'],
                'display_order': data['display_order'],
            }
        )
        print(f"{'Created' if created else 'Updated'} Pickup Location: {location.name} in {emirate.name}")

print("\nTest data has been added successfully!")
