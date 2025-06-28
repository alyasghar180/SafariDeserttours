#!/usr/bin/env python
"""
Script to import data into PostgreSQL database
"""
import os
import sys
import django

# Make sure we're using PostgreSQL
if 'USE_SQLITE' in os.environ:
    del os.environ['USE_SQLITE']
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.db import connections

# Verify we're using PostgreSQL
db_engine = settings.DATABASES['default']['ENGINE']
if 'postgresql' not in db_engine:
    print(f"❌ Not using PostgreSQL. Current engine: {db_engine}")
    print("Make sure USE_SQLITE environment variable is not set to 'True'")
    sys.exit(1)

print("Using database engine:", db_engine)
print("Database name:", settings.DATABASES['default']['NAME'])

# Step 1: Test PostgreSQL connection
print("\n[1/3] Testing PostgreSQL connection...")
try:
    connection = connections['default']
    connection.ensure_connection()
    print("✅ Successfully connected to PostgreSQL")
except Exception as e:
    print(f"❌ Error connecting to PostgreSQL: {str(e)}")
    print("Please check your PostgreSQL installation and settings.")
    sys.exit(1)

# Step 2: Apply migrations
print("\n[2/3] Applying migrations to PostgreSQL...")
try:
    call_command('migrate')
    print("✅ Successfully applied migrations")
except Exception as e:
    print(f"❌ Error applying migrations: {str(e)}")
    sys.exit(1)

# Step 3: Load data
print("\n[3/3] Loading data into PostgreSQL...")
try:
    call_command('loaddata', 'sqlite_data_backup.json')
    print("✅ Successfully loaded data into PostgreSQL")
except Exception as e:
    print(f"❌ Error loading data: {str(e)}")
    print("You may need to manually fix the data file and try again.")
    sys.exit(1)

print("\n✅ Migration completed successfully!")
print("\nNext steps:")
print("1. Test your application with PostgreSQL:")
print("   python manage.py runserver")
print("2. Verify that all your data is accessible in the application") 