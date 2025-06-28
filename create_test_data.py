import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

# Import models
from packages.models import PackageCategory, Package, PackageInclusion, PackageInclusionRelation

def create_test_data():
    print('Creating test data...')
    
    # Create categories
    print('Creating package categories...')
    standard = PackageCategory.objects.create(
        name='Standard Safari',
        slug='standard-safari',
        description='Our standard desert safari packages with essential experiences',
        icon='fas fa-sun',
        is_active=True
    )

    premium = PackageCategory.objects.create(
        name='Premium Safari',
        slug='premium-safari',
        description='Luxury desert experiences with premium amenities and services',
        icon='fas fa-crown',
        is_active=True
    )

    family = PackageCategory.objects.create(
        name='Family Safari',
        slug='family-safari',
        description='Family-friendly desert adventures suitable for all ages',
        icon='fas fa-users',
        is_active=True
    )
    
    # Create packages
    print('Creating packages...')
    evening_safari = Package.objects.create(
        name='Evening Desert Safari',
        slug='evening-desert-safari',
        category=standard,
        description='Experience the magic of the desert at sunset with our popular Evening Desert Safari package. This 6-hour adventure includes thrilling dune bashing, camel riding, sandboarding, and a delicious BBQ dinner under the stars with live entertainment.',
        short_description='Sunset adventure with BBQ dinner and entertainment',
        transportation_type='4x4',
        price=149.99,
        duration_hours=6,
        is_featured=True,
        is_active=True
    )

    vip_safari = Package.objects.create(
        name='VIP Luxury Safari',
        slug='vip-luxury-safari',
        category=premium,
        description='Indulge in our VIP Luxury Safari for the ultimate desert experience. Private 4x4 transportation, gourmet dinner, premium beverages, and exclusive entertainment in a luxurious setting.',
        short_description='Exclusive luxury experience with private transport',
        transportation_type='4x4',
        price=299.99,
        duration_hours=7,
        is_featured=True,
        is_active=True
    )

    family_safari = Package.objects.create(
        name='Family Adventure Safari',
        slug='family-adventure-safari',
        category=family,
        description='A perfect desert adventure for the whole family. Enjoy child-friendly dune bashing, camel rides, sandboarding, and a special kids entertainment program along with a family-style BBQ dinner.',
        short_description='Child-friendly adventure for the whole family',
        transportation_type='4x4',
        price=129.99,
        child_price=79.99,
        duration_hours=5,
        is_featured=True,
        is_active=True
    )
    
    # Create inclusions
    print('Creating package inclusions...')
    dune_bashing = PackageInclusion.objects.create(
        name='Dune Bashing', 
        description='Thrilling 4x4 dune bashing experience', 
        icon='fas fa-car'
    )
    camel_riding = PackageInclusion.objects.create(
        name='Camel Riding', 
        description='Traditional camel ride experience', 
        icon='fas fa-horse'
    )
    bbq_dinner = PackageInclusion.objects.create(
        name='BBQ Dinner', 
        description='Delicious BBQ buffet dinner with veg & non-veg options', 
        icon='fas fa-utensils'
    )
    entertainment = PackageInclusion.objects.create(
        name='Live Entertainment', 
        description='Belly dance, Tanura show, and Fire show', 
        icon='fas fa-theater-masks'
    )
    
    # Add inclusions to packages
    print('Adding inclusions to packages...')
    PackageInclusionRelation.objects.create(package=evening_safari, inclusion=dune_bashing)
    PackageInclusionRelation.objects.create(package=evening_safari, inclusion=camel_riding)
    PackageInclusionRelation.objects.create(package=evening_safari, inclusion=bbq_dinner)
    PackageInclusionRelation.objects.create(package=evening_safari, inclusion=entertainment)

    PackageInclusionRelation.objects.create(package=vip_safari, inclusion=dune_bashing)
    PackageInclusionRelation.objects.create(package=vip_safari, inclusion=camel_riding)
    PackageInclusionRelation.objects.create(package=vip_safari, inclusion=bbq_dinner)
    PackageInclusionRelation.objects.create(package=vip_safari, inclusion=entertainment)

    PackageInclusionRelation.objects.create(package=family_safari, inclusion=dune_bashing)
    PackageInclusionRelation.objects.create(package=family_safari, inclusion=camel_riding)
    PackageInclusionRelation.objects.create(package=family_safari, inclusion=bbq_dinner)
    PackageInclusionRelation.objects.create(package=family_safari, inclusion=entertainment)
    
    print('Test data creation completed!')

if __name__ == '__main__':
    create_test_data()
