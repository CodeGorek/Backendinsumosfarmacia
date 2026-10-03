"""
Configuración principal de Django para el proyecto.
Contiene las variables de entorno, configuración de base de datos, 
archivos estáticos, middleware y herramientas de terceros.
"""

from pathlib import Path

# Definición de la ruta base del directorio del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones de desarrollo (No aptas para entornos de producción).
# ADVERTENCIA DE SEGURIDAD: Clave secreta utilizada para firma criptográfica.
SECRET_KEY = 'django-insecure-jsyiku=ac)q#g*-s8)kewb)kymx+u*nf433r9f82is7aql8je1'

# ADVERTENCIA DE SEGURIDAD: Modo depuración habilitado (debe ser False en producción).
DEBUG = True

# Lista de dominios permitidos para alojar la aplicación.
ALLOWED_HOSTS = []

# ==========================================
# DEFINICIÓN DE APLICACIONES
# ==========================================

INSTALLED_APPS = [
    # Aplicaciones nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Herramientas de terceros requeridas por la arquitectura
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    
    # Aplicación principal del negocio
    'farmacia',
]

# Capas de middleware para procesamiento de peticiones y seguridad.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Archivo raíz de enrutamiento de URLs.
ROOT_URLCONF = 'config.urls'

# Configuración del motor de plantillas HTML (Templates).
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Archivo de entrada para despliegue WSGI.
WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# BASE DE DATOS
# ==========================================

# Configuración del motor de persistencia mediante PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'farmacia_db',
        'USER': 'postgres',
        'PASSWORD': 'postgre',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ==========================================
# VALIDACIÓN DE CONTRASEÑAS
# ==========================================

# Políticas de seguridad aplicadas a las contraseñas de los usuarios.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================================
# INTERNACIONALIZACIÓN
# ==========================================

# Configuración de idioma y zona horaria del sistema.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==========================================
# ARCHIVOS ESTÁTICOS
# ==========================================

# Configuración de ruta para archivos CSS, JavaScript e Imágenes.
STATIC_URL = '/static/'

# ==========================================
# CORREO ELECTRÓNICO
# ==========================================

# Configuración del servidor de envío de correos (salida por consola en desarrollo).
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# ==========================================
# CONFIGURACIONES DEL PROYECTO 5 (B2B)
# ==========================================

# 1. Autenticación: Definición explícita del modelo de usuario personalizado 
# para habilitar el uso de la propiedad 'rol' (Institución vs Gestor).
AUTH_USER_MODEL = 'farmacia.Usuario'

# 2. Configuración de Django REST Framework (DRF):
# - Integración de JWTAuthentication para validación de tokens de acceso en peticiones protegidas.
# - Habilitación de DjangoFilterBackend de forma global para búsquedas y filtros de catálogo.
# - Asignación de drf_spectacular como el motor generador de la documentación OpenAPI/Swagger.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# 3. Configuración de Documentación Swagger / OpenAPI:
# Definición de metadatos de la API, incluyendo los datos del desarrollador exigidos en la rúbrica.
SPECTACULAR_SETTINGS = {
    'TITLE': 'API Pedidos de Insumos Médicos',
    'DESCRIPTION': 'Desarrollado por: Oscar Javier Pérez Salazar | Sección: IEC-N4-C1 | Año: 2026. Plataforma B2B para clínicas e instituciones de salud.',
    'VERSION': '1.0.0',
}