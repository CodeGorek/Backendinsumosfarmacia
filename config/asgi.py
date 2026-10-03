"""
Módulo de configuración ASGI (Asynchronous Server Gateway Interface).
Expone la aplicación para servidores asíncronos (como Uvicorn o Daphne),
permitiendo la ejecución de WebSockets y tareas en segundo plano si se requiere.
"""
import os
from django.core.asgi import get_asgi_application

# Establecimiento de la variable de entorno para apuntar a las configuraciones globales.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Instanciación de la aplicación ASGI.
application = get_asgi_application()
