#!/usr/bin/env python
"""
PostgreSQL Database Restore Script for Safari Desert Tours

This script restores a PostgreSQL database from a backup file.
Usage: python restore_postgres.py <backup_file>
"""

import os
import subprocess
import sys
import datetime

# Configuration
DB_NAME = "safarideserttours"
DB_USER = "safari"
BACKUP_DIR = "backups"

def list_available_backups():
    """List all available backup files"""
    if not os.path.exists(BACKUP_DIR):
        print(f"Backup directory {BACKUP_DIR} does not exist.")
        return []
    
    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith(DB_NAME) and filename.endswith('.dump'):
            file_path = os.path.join(BACKUP_DIR, filename)
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            backups.append((filename, file_path, file_time, file_size))
    
    # Sort by time (newest first)
    backups.sort(key=lambda x: x[2], reverse=True)
    return backups

def print_available_backups(backups):
    """Print the list of available backups"""
    if not backups:
        print("No backup files found.")
        return
    
    print(f"\nAvailable backups in {BACKUP_DIR}:")
    print("-" * 80)
    print(f"{'#':<3} {'Backup File':<30} {'Date':<20} {'Size':<10}")
    print("-" * 80)
    
    for i, (filename, _, file_time, file_size) in enumerate(backups):
        print(f"{i+1:<3} {filename:<30} {file_time.strftime('%Y-%m-%d %H:%M:%S'):<20} {file_size:.2f} MB")

def restore_database(backup_file):
    """Restore the database from the backup file"""
    if not os.path.exists(backup_file):
        print(f"Error: Backup file {backup_file} does not exist.")
        return False
    
    print(f"\nRestoring database {DB_NAME} from {backup_file}...")
    print("WARNING: This will overwrite the current database!")
    
    confirm = input("Are you sure you want to continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Restore cancelled.")
        return False
    
    # Build the pg_restore command
    cmd = [
        "pg_restore",
        "-U", DB_USER,
        "-d", DB_NAME,
        "-c",  # Clean (drop) database objects before recreating
        backup_file
    ]
    
    try:
        # Run the restore command
        print(f"Starting restore of {DB_NAME} database...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Restore completed successfully!")
            return True
        else:
            print(f"❌ Restore completed with warnings/errors: {result.stderr}")
            print("The database may still be usable, but check for any issues.")
            return True
    except Exception as e:
        print(f"❌ Error during restore: {str(e)}")
        return False

def main():
    """Main function"""
    print(f"=== PostgreSQL Restore Script - {datetime.datetime.now()} ===")
    
    # Check if a backup file was specified
    if len(sys.argv) > 1:
        backup_file = sys.argv[1]
        if os.path.exists(backup_file):
            restore_database(backup_file)
        else:
            print(f"Error: Specified backup file {backup_file} does not exist.")
            sys.exit(1)
    else:
        # No backup file specified, list available backups
        backups = list_available_backups()
        print_available_backups(backups)
        
        if not backups:
            sys.exit(1)
        
        # Ask user to select a backup
        while True:
            try:
                choice = input("\nEnter the number of the backup to restore (or 'q' to quit): ")
                if choice.lower() == 'q':
                    print("Restore cancelled.")
                    sys.exit(0)
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(backups):
                    _, backup_path, _, _ = backups[choice_idx]
                    restore_database(backup_path)
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(backups)}.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main() 