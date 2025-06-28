#!/usr/bin/env python
"""
Script to export data from SQLite database
"""
import os
import sys
import django

# Set environment variable to use SQLite
os.environ['USE_SQLITE'] = 'True'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desert_safari.settings')
django.setup()

from django.core.management import call_command

print("Exporting data from SQLite database...")
try:
    call_command('dumpdata', 
                exclude=['contenttypes', 'auth.permission'],
                natural_foreign=True,
                natural_primary=True,
                indent=4,
                output='sqlite_data_backup.json')
    print(f"✅ Data exported successfully to sqlite_data_backup.json")
except Exception as e:
    print(f"❌ Error exporting data: {str(e)}")
    sys.exit(1) 