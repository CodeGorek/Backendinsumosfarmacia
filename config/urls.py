"""
Enrutador Principal (URLs) del Proyecto Django.
Gestión de rutas de la Interfaz Web (Frontend) y de la API REST (Backend).
Uso de DefaultRouter de DRF para generar las rutas CRUD de los ViewSets automáticamente.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from farmacia.views import (
    CustomTokenObtainPairView, InsumoViewSet, CarroViewSet, 
    TransaccionViewSet, CategoriaViewSet,
    home_view, custom_404_view, login_view, cliente_view, gestor_view
)

# Inicialización del router de DRF para la creación de endpoints de recursos
router = DefaultRouter()
router.register(r'insumos', InsumoViewSet, basename='insumo')
router.register(r'carro-insumos', CarroViewSet, basename='carro')
router.register(r'solicitudes', TransaccionViewSet, basename='solicitud')
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    # Ruta de acceso al panel de administración nativo de Django
    path('admin/', admin.site.urls),
    
    # Rutas dinámicas de los recursos de la API REST
    path('api/', include(router.urls)),
    
    # Endpoint especializado para Autenticación y Generación de Token JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Endpoints designados para Autodocumentación (Swagger / OpenAPI)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ==========================
    # Rutas Web (Templates HTML)
    # ==========================
    
    # Renderización del portal público
    path('', home_view, name='home'),
    
    # Renderización del formulario de acceso
    path('login/', login_view, name='login'),
    
    # Renderización de paneles de usuario
    path('cliente/', cliente_view, name='cliente'),
    path('gestor/', gestor_view, name='gestor'),
    
    # Interceptador (Catch-All) para manejar páginas no encontradas (404)
    re_path(r'^.*$', custom_404_view),
]