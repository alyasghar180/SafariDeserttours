# PostgreSQL Migration Guide for Safari Desert Tours

This guide provides step-by-step instructions for migrating the Safari Desert Tours application from SQLite to PostgreSQL.

## Prerequisites

1. PostgreSQL installed on your development/production server
2. Python packages:
   - psycopg2-binary
   - django-db-connection-pool

## Step 1: Install PostgreSQL

### Windows
1. Download PostgreSQL from the [official website](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the setup wizard
3. Remember the password you set for the postgres user
4. Add PostgreSQL bin directory to your PATH (typically `C:\Program Files\PostgreSQL\[version]\bin`)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

## Step 2: Create PostgreSQL Database and User

Run the following commands in PostgreSQL:

```sql
-- Create database
CREATE DATABASE safarideserttours;

-- Create user with password
CREATE USER safari WITH PASSWORD 'dubai@123';

-- Grant privileges
ALTER ROLE safari SET client_encoding TO 'utf8';
ALTER ROLE safari SET default_transaction_isolation TO 'read committed';
ALTER ROLE safari SET timezone TO 'UTC';

-- Grant all privileges on database
GRANT ALL PRIVILEGES ON DATABASE safarideserttours TO safari;

-- Connect to the new database to set up extensions and schema permissions
\c safarideserttours

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO safari;
```

You can run this SQL script using:
- **Windows**: `psql -U postgres -f create_db.sql`
- **Linux/macOS**: `sudo -u postgres psql -f create_db.sql`

## Step 3: Run the Migration Script

We've created a Python script that handles the migration process:

```bash
python migrate_to_postgres.py
```

This script will:
1. Backup data from the SQLite database
2. Switch to PostgreSQL configuration
3. Test the PostgreSQL connection
4. Apply migrations to PostgreSQL
5. Load data into PostgreSQL

## Step 4: Verify the Migration

After the migration is complete, verify that:

1. All data has been successfully transferred
2. The application works correctly with PostgreSQL
3. All relationships and constraints are preserved

Run the development server to test:

```bash
python manage.py runserver
```

## Step 5: Update Production Configuration

For production deployment:

1. Update your environment variables or settings to use PostgreSQL
2. Ensure your web server configuration is updated
3. Set up connection pooling for better performance

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure PostgreSQL is running
   - Check host, port, and firewall settings

2. **Authentication Failed**
   - Verify username and password
   - Check pg_hba.conf for authentication methods

3. **Data Migration Errors**
   - SQLite and PostgreSQL handle data types differently
   - Check for incompatible data or constraints

### Data Type Differences

Some data types are handled differently between SQLite and PostgreSQL:

- **Boolean**: SQLite uses 0/1, PostgreSQL uses true/false
- **Date/Time**: Format differences may cause issues
- **Text**: Character encoding differences (use UTF-8)
- **JSON**: PostgreSQL has native JSON support

## PostgreSQL Maintenance

### Regular Backups

Set up regular backups using pg_dump:

```bash
pg_dump -U safari -d safarideserttours -F c -f backup_filename.dump
```

### Restore from Backup

```bash
pg_restore -U safari -d safarideserttours -c backup_filename.dump
```

### Performance Tuning

Consider these PostgreSQL settings for better performance:

- Increase `shared_buffers` (typically 25% of system memory)
- Adjust `work_mem` for complex queries
- Set `effective_cache_size` to about 75% of system memory

## Connection Pooling

The application is already configured to use connection pooling in production via django-db-connection-pool.

Key settings:
- `POOL_SIZE`: 20 (default connections)
- `MAX_OVERFLOW`: 10 (additional connections when pool is full)
- `RECYCLE`: 300 (recycle connections after 5 minutes)

## References

- [Django PostgreSQL Documentation](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django DB Connection Pool](https://pypi.org/project/django-db-connection-pool/) 