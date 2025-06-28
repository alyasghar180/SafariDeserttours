from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from packages.models import Package
import os

class Command(BaseCommand):
    help = 'Updates the VIP Luxury Safari package with the specified image and details'

    def handle(self, *args, **options):
        try:
            # Get the VIP Luxury Safari package
            package = Package.objects.get(name='VIP Luxury Safari')
            
            # Update the package description
            package.short_description = 'Exclusive luxury experience with private transport'
            
            # Update the package duration if needed
            package.duration_hours = 7.0
            
            # Update the package with the image
            image_path = os.path.join('static', 'images', 'gallery', 'VIP Luxury Safari.jpeg')
            
            # Check if the image exists
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    package.featured_image.save('VIP Luxury Safari.jpeg', ImageFile(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated the image for {package.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Image file not found at {image_path}'))
                
            # Save the package
            package.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {package.name}'))
            
        except Package.DoesNotExist:
            self.stdout.write(self.style.ERROR('VIP Luxury Safari package not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating package: {str(e)}'))
