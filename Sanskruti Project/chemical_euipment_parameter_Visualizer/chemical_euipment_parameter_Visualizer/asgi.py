"""
ASGI config for chemical_euipment_parameter_Visualizer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chemical_euipment_parameter_Visualizer.settings')

application = get_asgi_application()
