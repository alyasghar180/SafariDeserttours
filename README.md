# Safari Desert Tours

A Django-based website for booking desert safari tours in Dubai.

## Features

- User registration and authentication
- Tour package browsing and booking
- Admin dashboard for managing bookings and packages
- SMS notifications for booking confirmations
- Location-based pickup options

## Tech Stack

- Django 5.2.1
- PostgreSQL
- Twilio for SMS notifications
- HTML/CSS/JavaScript

## Setup Instructions

### Prerequisites

- Python 3.x
- PostgreSQL
- Git

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/safarideserttours.git
   cd safarideserttours
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure the database
   - Create a PostgreSQL database
   - Update settings in `desert_safari/settings.py`

5. Run migrations
   ```
   python manage.py migrate
   ```

6. Create a superuser
   ```
   python manage.py createsuperuser
   ```

7. Run the development server
   ```
   python manage.py runserver
   ```

8. Access the site at http://127.0.0.1:8000/

## Email Configuration

See [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md) for email configuration instructions.

## PostgreSQL Migration

For PostgreSQL migration instructions, see [POSTGRESQL_MIGRATION_GUIDE.md](POSTGRESQL_MIGRATION_GUIDE.md). 