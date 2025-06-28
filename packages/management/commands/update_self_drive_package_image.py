from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from packages.models import Package
import os

class Command(BaseCommand):
    help = 'Updates the Trip Deal 2 Self Drive Package with the specified image and details'

    def handle(self, *args, **options):
        try:
            # Get the Trip Deal 2 Self Drive Package package
            package = Package.objects.get(name='Trip Deal 2 Self Drive Package')
            
            # Update the package description
            package.short_description = 'Self-drive to our desert camp and enjoy all activities.'
            
            # Update the package duration if needed
            package.duration_hours = 7.0
            
            # Update the package with the image
            image_path = os.path.join('static', 'images', 'gallery', 'Trip Deal 2 Self Drive Package.png')
            
            # Check if the image exists
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    package.featured_image.save('Trip Deal 2 Self Drive Package.png', ImageFile(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated the image for {package.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Image file not found at {image_path}'))
                
            # Save the package
            package.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {package.name}'))
            
        except Package.DoesNotExist:
            self.stdout.write(self.style.ERROR('Trip Deal 2 Self Drive Package not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating package: {str(e)}'))
