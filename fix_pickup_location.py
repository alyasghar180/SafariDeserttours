import os
import django
import sys
import sqlite3

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from django.conf import settings

# Get the database path from Django settings
db_path = settings.DATABASES['default']['NAME']

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute SQL to directly modify the column constraint
try:
    print("Starting database fix...")
    
    # Create a default pickup location to use for existing bookings
    from locations.models import PickupLocation, Emirate
    default_emirate, _ = Emirate.objects.get_or_create(
        name="Default", 
        defaults={"is_active": True, "display_order": 999}
    )
    
    default_pickup, _ = PickupLocation.objects.get_or_create(
        name="Default Location",
        emirate=default_emirate,
        defaults={
            "is_active": True,
            "display_order": 999,
            "additional_cost": 0
        }
    )
    
    print(f"Created default pickup location with ID: {default_pickup.id}")
    
    # Update all existing bookings to use the default pickup location
    cursor.execute(f"UPDATE bookings_booking SET pickup_location_id = {default_pickup.id} WHERE pickup_location_id IS NULL;")
    
    # Commit the changes
    conn.commit()
    print("Database fix completed successfully!")
    
except Exception as e:
    # Rollback in case of error
    conn.rollback()
    print(f"Error fixing database: {str(e)}")
finally:
    # Close the connection
    conn.close()
