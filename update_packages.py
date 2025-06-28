import os
import django
import sys
from decimal import Decimal
from datetime import time

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

# Import models
from packages.models import (
    Package, 
    PackageCategory, 
    PackageInclusion, 
    PackageInclusionRelation,
    PackageAddon,
    PackageAddonRelation
)

# Create or get package categories
standard_category, _ = PackageCategory.objects.get_or_create(
    name="Standard Safari",
    defaults={
        'description': 'Our standard desert safari packages offering great value.',
        'icon': 'fa-star',
    }
)

budget_category, _ = PackageCategory.objects.get_or_create(
    name="Budget Safari",
    defaults={
        'description': 'Affordable desert safari experiences for budget-conscious travelers.',
        'icon': 'fa-money-bill',
    }
)

premium_category, _ = PackageCategory.objects.get_or_create(
    name="Premium Safari",
    defaults={
        'description': 'Premium desert safari experiences with luxury amenities.',
        'icon': 'fa-gem',
    }
)

# Create or update inclusions
inclusions = {
    'dune_bashing': PackageInclusion.objects.get_or_create(
        name="Dune Bashing",
        defaults={
            'description': 'Experience the thrill of driving over sand dunes.',
            'icon': 'fa-car',
            'display_order': 1,
        }
    )[0],
    'camel_riding': PackageInclusion.objects.get_or_create(
        name="Camel Riding",
        defaults={
            'description': 'Enjoy a traditional camel ride in the desert.',
            'icon': 'fa-horse',
            'display_order': 2,
        }
    )[0],
    'sand_boarding': PackageInclusion.objects.get_or_create(
        name="Sand Boarding",
        defaults={
            'description': 'Slide down the sand dunes on a board.',
            'icon': 'fa-snowboarding',
            'display_order': 3,
        }
    )[0],
    'bbq_dinner': PackageInclusion.objects.get_or_create(
        name="BBQ Buffet Dinner",
        defaults={
            'description': 'Enjoy a delicious BBQ buffet dinner with various options.',
            'icon': 'fa-utensils',
            'display_order': 4,
        }
    )[0],
    'henna_tattoo': PackageInclusion.objects.get_or_create(
        name="Henna Tattoo",
        defaults={
            'description': 'Get a traditional henna tattoo design.',
            'icon': 'fa-paint-brush',
            'display_order': 5,
        }
    )[0],
    'sheesha': PackageInclusion.objects.get_or_create(
        name="Sheesha",
        defaults={
            'description': 'Try traditional Arabic water pipe.',
            'icon': 'fa-smoking',
            'display_order': 6,
        }
    )[0],
    'arabic_dress': PackageInclusion.objects.get_or_create(
        name="Arabic Dress",
        defaults={
            'description': 'Try on traditional Arabic clothing for photos.',
            'icon': 'fa-tshirt',
            'display_order': 7,
        }
    )[0],
    'soft_drinks': PackageInclusion.objects.get_or_create(
        name="Soft Drinks",
        defaults={
            'description': 'Unlimited soft drinks included.',
            'icon': 'fa-glass-whiskey',
            'display_order': 8,
        }
    )[0],
    'water': PackageInclusion.objects.get_or_create(
        name="Water",
        defaults={
            'description': 'Bottled water included.',
            'icon': 'fa-tint',
            'display_order': 9,
        }
    )[0],
    'tea_coffee': PackageInclusion.objects.get_or_create(
        name="Tea & Coffee",
        defaults={
            'description': 'Enjoy traditional Arabic tea and coffee.',
            'icon': 'fa-coffee',
            'display_order': 10,
        }
    )[0],
    'belly_dance': PackageInclusion.objects.get_or_create(
        name="Belly Dance Show",
        defaults={
            'description': 'Watch a professional belly dance performance.',
            'icon': 'fa-music',
            'display_order': 11,
        }
    )[0],
    'fire_show': PackageInclusion.objects.get_or_create(
        name="Fire Show",
        defaults={
            'description': 'Be amazed by a spectacular fire performance.',
            'icon': 'fa-fire',
            'display_order': 12,
        }
    )[0],
    'tanura_show': PackageInclusion.objects.get_or_create(
        name="Tanura Show",
        defaults={
            'description': 'Experience the traditional Tanura dance performance.',
            'icon': 'fa-compact-disc',
            'display_order': 13,
        }
    )[0],
}

# Create or update addons
quad_bike_addon, _ = PackageAddon.objects.get_or_create(
    name="Quad Bike Ride",
    defaults={
        'description': 'Experience the thrill of riding a quad bike in the desert.',
        'price': Decimal('85.00'),
        'is_per_person': True,
        'icon': 'fa-motorcycle',
    }
)

# Create or update packages

# 1. Self Drive Package
self_drive_package, created = Package.objects.update_or_create(
    name="Trip Deal 2 Self Drive Package",
    defaults={
        'category': budget_category,
        'description': (
            "Come by your own car to our desert camp location. "
            "This budget-friendly option lets you experience the magic of the desert "
            "while arranging your own transportation to our camp."
        ),
        'short_description': "Self-drive to our desert camp and enjoy all activities.",
        'transportation_type': 'self_drive',
        'price': Decimal('40.00'),
        'child_price': Decimal('40.00'),
        'duration_hours': Decimal('7.0'),
        'pickup_time_start': time(14, 0),  # 2:00 PM
        'pickup_time_end': time(14, 30),   # 2:30 PM
        'dropoff_time_start': time(21, 0), # 9:00 PM
        'dropoff_time_end': time(21, 30),  # 9:30 PM
        'is_active': True,
    }
)

# 2. Bus Transportation Package
bus_package, created = Package.objects.update_or_create(
    name="Desert Safari Bus Transportation",
    defaults={
        'category': standard_category,
        'description': (
            "Experience the desert safari with convenient bus transportation from various pickup points "
            "across Dubai, Sharjah, and Ajman. Enjoy all the desert activities and shows with comfortable "
            "transportation included."
        ),
        'short_description': "Desert safari with bus transportation from central pickup points.",
        'transportation_type': 'bus',
        'price': Decimal('45.00'),
        'child_price': Decimal('45.00'),
        'duration_hours': Decimal('7.0'),
        'pickup_time_start': time(14, 0),  # 2:00 PM
        'pickup_time_end': time(14, 30),   # 2:30 PM
        'dropoff_time_start': time(21, 0), # 9:00 PM
        'dropoff_time_end': time(21, 30),  # 9:30 PM
        'is_active': True,
    }
)

# 3. 4x4 Transportation Package
premium_package, created = Package.objects.update_or_create(
    name="Premium 4x4 Desert Safari",
    defaults={
        'category': premium_category,
        'description': (
            "Experience the ultimate desert safari with our premium 4x4 transportation. "
            "Enjoy pickup and drop-off in a comfortable 4x4 vehicle, plus all the exciting "
            "desert activities and entertainment."
        ),
        'short_description': "Premium desert safari experience with 4x4 transportation.",
        'transportation_type': '4x4',
        'price': Decimal('110.00'),
        'child_price': Decimal('110.00'),
        'duration_hours': Decimal('7.0'),
        'pickup_time_start': time(14, 0),  # 2:00 PM
        'pickup_time_end': time(16, 0),    # 4:00 PM (wider window for premium service)
        'dropoff_time_start': time(20, 0), # 8:00 PM
        'dropoff_time_end': time(22, 0),   # 10:00 PM
        'is_active': True,
    }
)

# Add inclusions to packages
all_packages = [self_drive_package, bus_package, premium_package]
all_inclusions = list(inclusions.values())

for package in all_packages:
    # Clear existing inclusions
    PackageInclusionRelation.objects.filter(package=package).delete()
    
    # Add all inclusions to each package
    for inclusion in all_inclusions:
        PackageInclusionRelation.objects.create(
            package=package,
            inclusion=inclusion
        )

# Add quad bike addon to all packages
for package in all_packages:
    # Clear existing addon relations
    PackageAddonRelation.objects.filter(package=package, addon=quad_bike_addon).delete()
    
    # Add quad bike addon with appropriate pricing
    PackageAddonRelation.objects.create(
        package=package,
        addon=quad_bike_addon,
        special_price=Decimal('85.00')  # As per your requirements
    )

print("Packages updated successfully!")
print("Current packages:")
for p in Package.objects.all():
    print(f"- {p.name}: {p.price} AED ({p.get_transportation_type_display()})")


# Add inclusions to packages
all_packages = [self_drive_package, bus_package, premium_package]
all_inclusions = list(inclusions.values())

for package in all_packages:
    # Clear existing inclusions
    PackageInclusionRelation.objects.filter(package=package).delete()
    
    # Add all inclusions to each package
    for inclusion in all_inclusions:
        PackageInclusionRelation.objects.create(
            package=package,
            inclusion=inclusion
        )

# Add quad bike addon to all packages
for package in all_packages:
    # Clear existing addon relations
    PackageAddonRelation.objects.filter(package=package, addon=quad_bike_addon).delete()
    
    # Add quad bike addon with appropriate pricing
    PackageAddonRelation.objects.create(
        package=package,
        addon=quad_bike_addon,
        special_price=Decimal('85.00')  # As per your requirements
    )

print("Packages updated successfully!")
print("Current packages:")
for p in Package.objects.all():
    print(f"- {p.name}: {p.price} AED ({p.get_transportation_type_display()})")
