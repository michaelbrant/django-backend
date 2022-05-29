"""
WSGI config for agrawat_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from .utils.get_env_settings import get_env_settings_file_name
from dotenv import load_dotenv

load_dotenv()
settings_file = get_env_settings_file_name()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)

application = get_wsgi_application()
