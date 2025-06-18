#!/usr/bin/env python3
"""
Passenger WSGI file for Plesk hosting
This file should be placed in the root directory of your Django project
(same level as manage.py)
"""

import os
import sys
from pathlib import Path

# Get the directory where this file is located (project root)
BASE_DIR = Path(__file__).resolve().parent

# Add the project root directory to Python path
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Add the parent directory if needed (for import resolution)
if str(BASE_DIR.parent) not in sys.path:
    sys.path.insert(0, str(BASE_DIR.parent))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tawheedUmrahBack.settings')

try:
    # Import Django and configure it
    import django
    from django.core.wsgi import get_wsgi_application
    
    # Configure Django settings
    django.setup()
    
    # Create WSGI application
    application = get_wsgi_application()
    
except ImportError as e:
    # Fallback error handling
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f'Django import error: {str(e)}'.encode('utf-8')]

# For debugging purposes (remove in production)
def debug_application(environ, start_response):
    """Debug wrapper to help troubleshoot issues"""
    try:
        return application(environ, start_response)
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        error_msg = f'''
Error: {str(e)}
Python Path: {sys.path}
Working Directory: {os.getcwd()}
BASE_DIR: {BASE_DIR}
Environment: {dict(os.environ)}
'''
        return [error_msg.encode('utf-8')]

# Uncomment the line below if you need debugging (comment out in production)
# application = debug_application