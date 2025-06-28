#!/usr/bin/env python
"""
Script to migrate data from SQLite to PostgreSQL for Safari Desert Tours.
This script:
1. Dumps data from SQLite database
2. Adjusts the database settings to use PostgreSQL
3. Applies migrations to the PostgreSQL database
4. Loads data into the PostgreSQL database
"""

import os
import subprocess
import sys
import time

# Set up Django environment
import django
from django.conf import settings
from django.core.management import call_command

def main():
    print("Starting migration from SQLite to PostgreSQL...")
    
    # Step 1: Backup the SQLite database
    print("\n[1/5] Creating backup of SQLite database...")
    sqlite_backup_file = "sqlite_data_backup.json"
    
    try:
        # Set environment variable to use SQLite
        os.environ['USE_SQLITE'] = 'True'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
        django.setup()
        
        # Dump data excluding contenttypes and auth.permission
        call_command('dumpdata', 
                    exclude=['contenttypes', 'auth.permission'],
                    natural_foreign=True,
                    natural_primary=True,
                    indent=4,
                    output=sqlite_backup_file)
        
        print(f"✅ SQLite data backed up to {sqlite_backup_file}")
    except Exception as e:
        print(f"❌ Error backing up SQLite data: {str(e)}")
        sys.exit(1)
    
    # Step 2: Switch to PostgreSQL configuration
    print("\n[2/5] Switching to PostgreSQL configuration...")
    try:
        # Unset the SQLite environment variable to use PostgreSQL
        if 'USE_SQLITE' in os.environ:
            del os.environ['USE_SQLITE']
        
        # Reload Django settings to use PostgreSQL
        django.setup()
        
        # Verify we're using PostgreSQL
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'postgresql' not in db_engine:
            print(f"❌ Not using PostgreSQL. Current engine: {db_engine}")
            sys.exit(1)
        
        print(f"✅ Successfully switched to PostgreSQL configuration")
    except Exception as e:
        print(f"❌ Error switching to PostgreSQL: {str(e)}")
        sys.exit(1)
    
    # Step 3: Check PostgreSQL connection
    print("\n[3/5] Testing PostgreSQL connection...")
    try:
        from django.db import connections
        connection = connections['default']
        connection.ensure_connection()
        print("✅ Successfully connected to PostgreSQL")
    except Exception as e:
        print(f"❌ Error connecting to PostgreSQL: {str(e)}")
        print("Please make sure PostgreSQL is running and the database exists.")
        sys.exit(1)
    
    # Step 4: Apply migrations to PostgreSQL
    print("\n[4/5] Applying migrations to PostgreSQL...")
    try:
        call_command('migrate')
        print("✅ Successfully applied migrations to PostgreSQL")
    except Exception as e:
        print(f"❌ Error applying migrations: {str(e)}")
        sys.exit(1)
    
    # Step 5: Load data into PostgreSQL
    print("\n[5/5] Loading data into PostgreSQL...")
    try:
        call_command('loaddata', sqlite_backup_file)
        print("✅ Successfully loaded data into PostgreSQL")
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        print("You may need to manually fix the data file and try again.")
        sys.exit(1)
    
    print("\n✅ Migration completed successfully!")
    print("\nNext steps:")
    print("1. Test your application with the new PostgreSQL database")
    print("2. Update your production deployment configuration")
    print("3. Consider setting up regular PostgreSQL backups")

if __name__ == "__main__":
    main() 