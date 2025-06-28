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
    print("Starting direct database fix...")
    
    # First, check if there are any existing bookings
    cursor.execute("SELECT COUNT(*) FROM bookings_booking;")
    booking_count = cursor.fetchone()[0]
    print(f"Found {booking_count} existing bookings")
    
    # Execute a direct SQL command to modify the table schema
    cursor.execute("PRAGMA foreign_keys=off;")
    
    # Get the current table schema
    cursor.execute("PRAGMA table_info(bookings_booking);")
    columns = cursor.fetchall()
    print("Current table schema:")
    for col in columns:
        print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}")
    
    # Create a temporary table with the correct schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings_booking_temp (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id VARCHAR(50) NOT NULL UNIQUE,
        status VARCHAR(20) NOT NULL,
        booking_date DATE NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(254) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        nationality VARCHAR(50) NOT NULL,
        adults SMALLINT UNSIGNED NOT NULL,
        children SMALLINT UNSIGNED NOT NULL,
        pickup_location_text VARCHAR(255) NOT NULL,
        pickup_time TIME NULL,
        hotel_name VARCHAR(100) NOT NULL,
        hotel_room VARCHAR(20) NOT NULL,
        address_details TEXT NOT NULL,
        special_requests TEXT NOT NULL,
        payment_method VARCHAR(20) NOT NULL,
        total_price DECIMAL NOT NULL,
        payment_id VARCHAR(100) NOT NULL,
        is_paid BOOL NOT NULL,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        cancelled_at DATETIME NULL,
        cancellation_reason TEXT NOT NULL,
        emirate_id INTEGER NULL REFERENCES locations_emirate(id),
        package_id INTEGER NOT NULL REFERENCES packages_package(id),
        pickup_location_id INTEGER NULL REFERENCES locations_pickuplocation(id),
        user_id INTEGER NULL REFERENCES accounts_customuser(id)
    );
    """)
    
    # Copy data from the original table to the temporary table
    cursor.execute("""
    INSERT OR IGNORE INTO bookings_booking_temp 
    SELECT * FROM bookings_booking;
    """)
    
    # Drop the original table
    cursor.execute("DROP TABLE IF EXISTS bookings_booking;")
    
    # Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE bookings_booking_temp RENAME TO bookings_booking;")
    
    # Re-create the indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS bookings_booking_emirate_id_4c9f9e2c ON bookings_booking(emirate_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS bookings_booking_package_id_8b3b5201 ON bookings_booking(package_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS bookings_booking_pickup_location_id_e6e79d9a ON bookings_booking(pickup_location_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS bookings_booking_user_id_e5c3db0d ON bookings_booking(user_id);")
    
    # Re-enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys=on;")
    
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
