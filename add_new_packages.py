import os
import django
import sys

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from packages.models import Package, PackageCategory

def create_city_tours_category():
    # Create City Tours category if it doesn't exist
    city_tours, created = PackageCategory.objects.get_or_create(
        name='City Tours',
        defaults={
            'description': 'Explore the beautiful cities of UAE',
            'icon': 'fa-city',
            'is_active': True
        }
    )
    
    if created:
        print("Created City Tours category")
    else:
        print("City Tours category already exists")
    
    return city_tours

def create_dubai_city_tour(category):
    # Create Dubai City Tour package
    dubai_tour, created = Package.objects.get_or_create(
        name='Dubai City Tour (Private)',
        defaults={
            'category': category,
            'description': 'Explore the vibrant city of Dubai with our private city tour. Visit iconic landmarks including Burj Khalifa, Dubai Mall, Palm Jumeirah, and Dubai Marina.',
            'short_description': 'Private tour of Dubai\'s most iconic landmarks and attractions',
            'transportation_type': '4x4',  # Using 4x4 as the transportation type
            'price': 350.00,  # Starting price
            'duration_hours': 8.00,
            'is_active': True
        }
    )
    
    if created:
        print("Created Dubai City Tour package")
    else:
        print("Dubai City Tour package already exists")
        
    # Create full day option
    dubai_full_day, created = Package.objects.get_or_create(
        name='Dubai City Tour (Full Day)',
        defaults={
            'category': category,
            'description': 'Experience the best of Dubai in our comprehensive full-day tour. Visit all major attractions including Burj Khalifa, Dubai Mall, Palm Jumeirah, Dubai Marina, Gold Souk, and more.',
            'short_description': 'Comprehensive full-day tour covering all major Dubai attractions',
            'transportation_type': '4x4',
            'price': 650.00,
            'duration_hours': 12.00,
            'is_active': True
        }
    )
    
    if created:
        print("Created Dubai Full Day Tour package")
    else:
        print("Dubai Full Day Tour package already exists")

def create_abu_dhabi_tour(category):
    # Create Abu Dhabi Tour package
    abu_dhabi_tour, created = Package.objects.get_or_create(
        name='Abu Dhabi Tour (7-seater)',
        defaults={
            'category': category,
            'description': 'Discover the capital city of UAE with our comfortable 7-seater vehicle. Visit Sheikh Zayed Grand Mosque, Emirates Palace, Qasr Al Watan, and other iconic landmarks.',
            'short_description': 'Explore Abu Dhabi\'s cultural and architectural wonders in a spacious 7-seater',
            'transportation_type': '4x4',
            'price': 850.00,
            'duration_hours': 10.00,
            'is_active': True
        }
    )
    
    if created:
        print("Created Abu Dhabi Tour (7-seater) package")
    else:
        print("Abu Dhabi Tour (7-seater) package already exists")
    
    # Create luxury 5-seater option
    abu_dhabi_luxury, created = Package.objects.get_or_create(
        name='Abu Dhabi Tour (Luxury 5-seater)',
        defaults={
            'category': category,
            'description': 'Experience Abu Dhabi in style with our luxury 5-seater vehicle. Enjoy a premium tour of Sheikh Zayed Grand Mosque, Emirates Palace, Qasr Al Watan, and other iconic landmarks.',
            'short_description': 'Premium Abu Dhabi experience in a luxury 5-seater vehicle',
            'transportation_type': '4x4',
            'price': 950.00,
            'duration_hours': 10.00,
            'is_active': True
        }
    )
    
    if created:
        print("Created Abu Dhabi Tour (Luxury 5-seater) package")
    else:
        print("Abu Dhabi Tour (Luxury 5-seater) package already exists")

if __name__ == "__main__":
    print("Adding new packages...")
    
    # Create category
    city_tours_category = create_city_tours_category()
    
    # Create packages
    create_dubai_city_tour(city_tours_category)
    create_abu_dhabi_tour(city_tours_category)
    
    print("Done!") 