import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from packages.models import PackageCategory, Package, PackageInclusion, PackageInclusionRelation

# Create categories
print('Creating package categories...')
categories = {
    'standard': PackageCategory.objects.create(
        name='Standard Safari',
        slug='standard-safari',
        description='Our standard desert safari packages with essential experiences',
        icon='fas fa-sun',
        is_active=True
    ),
    'premium': PackageCategory.objects.create(
        name='Premium Safari',
        slug='premium-safari',
        description='Luxury desert experiences with premium amenities and services',
        icon='fas fa-crown',
        is_active=True
    ),
    'family': PackageCategory.objects.create(
        name='Family Safari',
        slug='family-safari',
        description='Family-friendly desert adventures suitable for all ages',
        icon='fas fa-users',
        is_active=True
    )
}

# Create packages
print('Creating packages...')
packages = [
    Package.objects.create(
        name='Evening Desert Safari',
        slug='evening-desert-safari',
        category=categories['standard'],
        description='Experience the magic of the desert at sunset with our popular Evening Desert Safari package. This 6-hour adventure includes thrilling dune bashing, camel riding, sandboarding, and a delicious BBQ dinner under the stars with live entertainment.',
        short_description='Sunset adventure with BBQ dinner and entertainment',
        transportation_type='4x4',
        price=149.99,
        duration_hours=6,
        is_featured=True,
        is_active=True
    ),
    Package.objects.create(
        name='Morning Desert Safari',
        slug='morning-desert-safari',
        category=categories['standard'],
        description='Start your day with an exciting Morning Desert Safari. Experience the beauty of the desert in the morning light, enjoy dune bashing, camel riding, and sandboarding in cooler temperatures.',
        short_description='Morning adventure in cooler temperatures',
        transportation_type='4x4',
        price=99.99,
        duration_hours=4,
        is_featured=False,
        is_active=True
    ),
    Package.objects.create(
        name='VIP Luxury Safari',
        slug='vip-luxury-safari',
        category=categories['premium'],
        description='Indulge in our VIP Luxury Safari for the ultimate desert experience. Private 4x4 transportation, gourmet dinner, premium beverages, and exclusive entertainment in a luxurious setting.',
        short_description='Exclusive luxury experience with private transport',
        transportation_type='4x4',
        price=299.99,
        duration_hours=7,
        is_featured=True,
        is_active=True
    ),
    Package.objects.create(
        name='Family Adventure Safari',
        slug='family-adventure-safari',
        category=categories['family'],
        description='A perfect desert adventure for the whole family. Enjoy child-friendly dune bashing, camel rides, sandboarding, and a special kids entertainment program along with a family-style BBQ dinner.',
        short_description='Child-friendly adventure for the whole family',
        transportation_type='4x4',
        price=129.99,
        child_price=79.99,
        duration_hours=5,
        is_featured=True,
        is_active=True
    ),
    Package.objects.create(
        name='Self-Drive Camp Experience',
        slug='self-drive-camp-experience',
        category=categories['standard'],
        description='Drive your own vehicle to our desert camp and enjoy all the activities and entertainment without the dune bashing experience. Perfect for those who prefer to drive themselves.',
        short_description='Use your own vehicle to reach our camp',
        transportation_type='self_drive',
        price=79.99,
        duration_hours=5,
        is_featured=False,
        is_active=True
    ),
    Package.objects.create(
        name='Overnight Desert Camping',
        slug='overnight-desert-camping',
        category=categories['premium'],
        description='Experience the true magic of the desert with our Overnight Camping Safari. Enjoy all the activities of the evening safari plus sleeping under the stars in traditional Bedouin tents and breakfast in the morning.',
        short_description='Sleep under the stars in Bedouin tents',
        transportation_type='4x4',
        price=249.99,
        duration_hours=16,
        is_featured=True,
        is_active=True
    )
]

# Create inclusions
print('Creating package inclusions...')
inclusions = [
    PackageInclusion.objects.create(name='Dune Bashing', description='Thrilling 4x4 dune bashing experience', icon='fas fa-car'),
    PackageInclusion.objects.create(name='Camel Riding', description='Traditional camel ride experience', icon='fas fa-horse'),
    PackageInclusion.objects.create(name='Sandboarding', description='Exciting sand boarding down the dunes', icon='fas fa-snowboarding'),
    PackageInclusion.objects.create(name='BBQ Dinner', description='Delicious BBQ buffet dinner with veg & non-veg options', icon='fas fa-utensils'),
    PackageInclusion.objects.create(name='Live Entertainment', description='Belly dance, Tanura show, and Fire show', icon='fas fa-theater-masks'),
    PackageInclusion.objects.create(name='Henna Painting', description='Traditional henna painting', icon='fas fa-paint-brush'),
    PackageInclusion.objects.create(name='Shisha Smoking', description='Traditional Arabic water pipe', icon='fas fa-smoking'),
    PackageInclusion.objects.create(name='Arabic Costumes', description='Try on traditional Arabic costumes for photos', icon='fas fa-tshirt'),
    PackageInclusion.objects.create(name='Unlimited Soft Drinks', description='Unlimited soft drinks, water, tea, and coffee', icon='fas fa-coffee'),
    PackageInclusion.objects.create(name='Pickup & Drop-off', description='Hotel pickup and drop-off included', icon='fas fa-shuttle-van')
]

# Add inclusions to packages
print('Adding inclusions to packages...')
# Evening Desert Safari inclusions
for inclusion in [inclusions[0], inclusions[1], inclusions[2], inclusions[3], inclusions[4], inclusions[5], inclusions[6], inclusions[7], inclusions[8]]:
    PackageInclusionRelation.objects.create(package=packages[0], inclusion=inclusion)

# Morning Desert Safari inclusions
for inclusion in [inclusions[0], inclusions[1], inclusions[2], inclusions[8]]:
    PackageInclusionRelation.objects.create(package=packages[1], inclusion=inclusion)

# VIP Luxury Safari inclusions
for inclusion in inclusions:
    PackageInclusionRelation.objects.create(package=packages[2], inclusion=inclusion)

# Family Adventure Safari inclusions
for inclusion in [inclusions[0], inclusions[1], inclusions[2], inclusions[3], inclusions[4], inclusions[5], inclusions[7], inclusions[8], inclusions[9]]:
    PackageInclusionRelation.objects.create(package=packages[3], inclusion=inclusion)

# Self-Drive Camp Experience inclusions
for inclusion in [inclusions[1], inclusions[2], inclusions[3], inclusions[4], inclusions[5], inclusions[6], inclusions[7], inclusions[8]]:
    PackageInclusionRelation.objects.create(package=packages[4], inclusion=inclusion)

# Overnight Desert Camping inclusions
for inclusion in inclusions:
    PackageInclusionRelation.objects.create(package=packages[5], inclusion=inclusion)

print('Test data creation completed!')
