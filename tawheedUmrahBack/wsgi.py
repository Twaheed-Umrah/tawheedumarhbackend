"""
WSGI config for tawheedUmrahBack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import sys
import os

# Adjust the path to point to your project root
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tawheedUmrahBack.settings')

# Import application from Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
