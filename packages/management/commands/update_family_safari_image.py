from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from packages.models import Package
import os

class Command(BaseCommand):
    help = 'Updates the Family Adventure Safari package with the specified image'

    def handle(self, *args, **options):
        try:
            # Get the Family Adventure Safari package
            package = Package.objects.get(name='Family Adventure Safari')
            
            # Update the package description
            package.short_description = 'Child-friendly adventure for the whole family'
            
            # Update the package with the image
            image_path = os.path.join('static', 'images', 'gallery', 'Family Adventure Safari.png')
            
            # Check if the image exists
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    package.featured_image.save('Family Adventure Safari.png', ImageFile(f), save=True)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated the image for {package.name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Image file not found at {image_path}'))
                
            # Save the package
            package.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {package.name}'))
            
        except Package.DoesNotExist:
            self.stdout.write(self.style.ERROR('Family Adventure Safari package not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error updating package: {str(e)}'))
