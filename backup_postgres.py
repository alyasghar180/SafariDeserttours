#!/usr/bin/env python
"""
PostgreSQL Database Backup Script for Safari Desert Tours

This script creates a backup of the PostgreSQL database and stores it
in a timestamped file. It can be scheduled to run regularly using cron
or Windows Task Scheduler.
"""

import os
import subprocess
import datetime
import sys

# Configuration
DB_NAME = "safarideserttours"
DB_USER = "safari"
BACKUP_DIR = "backups"
BACKUP_RETENTION_DAYS = 30  # Number of days to keep backups

def create_backup_dir():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")

def perform_backup():
    """Perform the database backup"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_{timestamp}.dump")
    
    # Build the pg_dump command
    cmd = [
        "pg_dump",
        "-U", DB_USER,
        "-d", DB_NAME,
        "-F", "c",  # Custom format (compressed)
        "-f", backup_file
    ]
    
    try:
        # Run the backup command
        print(f"Starting backup of {DB_NAME} database...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Backup completed successfully: {backup_file}")
            return True
        else:
            print(f"❌ Backup failed with error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error during backup: {str(e)}")
        return False

def cleanup_old_backups():
    """Delete backups older than BACKUP_RETENTION_DAYS"""
    print(f"Cleaning up backups older than {BACKUP_RETENTION_DAYS} days...")
    
    current_time = datetime.datetime.now()
    retention_delta = datetime.timedelta(days=BACKUP_RETENTION_DAYS)
    
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith(DB_NAME) and filename.endswith('.dump'):
            file_path = os.path.join(BACKUP_DIR, filename)
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if current_time - file_time > retention_delta:
                try:
                    os.remove(file_path)
                    print(f"Deleted old backup: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {str(e)}")

def main():
    """Main function"""
    print(f"=== PostgreSQL Backup Script - {datetime.datetime.now()} ===")
    
    # Create backup directory if needed
    create_backup_dir()
    
    # Perform the backup
    success = perform_backup()
    
    # Clean up old backups if backup was successful
    if success:
        cleanup_old_backups()
    
    print("Backup process completed.")

if __name__ == "__main__":
    main() 