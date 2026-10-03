"""
Módulo de configuración WSGI (Web Server Gateway Interface).
Expone la aplicación como una función a nivel de módulo que los servidores web
(como Gunicorn o Apache) utilizan para comunicarse con Django de forma síncrona.
"""
import os
from django.core.wsgi import get_wsgi_application

# Establecimiento de la variable de entorno para apuntar a las configuraciones globales.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Instanciación de la aplicación WSGI.
application = get_wsgi_application()
