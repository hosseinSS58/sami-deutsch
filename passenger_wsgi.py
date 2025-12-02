"""
Passenger WSGI file for cPanel deployment.

This file is required for deploying Django applications on cPanel using Passenger.
Place this file in the root directory of your project (same level as manage.py).
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sami.settings')

# Initialize Django
django.setup()

# Import the WSGI application
from sami.wsgi import application

# Passenger requires this variable
# DO NOT REMOVE THIS LINE
application = application






