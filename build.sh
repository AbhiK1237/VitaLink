#!/usr/bin/env bash
# exit on error
set -o errexit

# Ensure Python 3.11.8 is used
python3.11 --version

# Create a Python virtual environment with Python 3.11.8
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install --upgrade djangorestframework-simplejwt
pip install Django==4.1.13

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
