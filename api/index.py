import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "industry5.0.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()