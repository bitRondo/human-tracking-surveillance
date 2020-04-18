"""
WSGI config for HumanTrackingSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#from videoAnalysis.videoAnalysis import runMain

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HumanTrackingSystem.settings')

application = get_wsgi_application()

# Uncomment the following line to load background processes which are in videoAnalysis module
# runMain()
