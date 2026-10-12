#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create superuser (if env vars set)
python manage.py createsuperuser --no-input || echo "Superuser already exists"