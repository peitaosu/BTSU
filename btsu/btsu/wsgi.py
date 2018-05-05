"""
WSGI config for btsu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if app_path not in sys.path:
    sys.path.append(app_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "btsu.settings")

application = get_wsgi_application()
