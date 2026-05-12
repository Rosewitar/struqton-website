"""
WSGI config for Struqton Structural project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'struqton_project.settings')
application = get_wsgi_application()
