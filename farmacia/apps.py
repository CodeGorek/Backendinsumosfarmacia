"""
Módulo de inicialización de la aplicación 'farmacia'.
Configura los metadatos básicos de la aplicación dentro del proyecto Django.
"""
from django.apps import AppConfig

class FarmaciaConfig(AppConfig):
    """
    Configuración de la aplicación principal.
    Define el tipo de campo automático para las claves primarias (BigAuto) 
    y el nombre interno del módulo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'farmacia'
