"""
Módulo de Vistas de la aplicación farmacia.
Contiene las vistas basadas en clases para la API REST (mediante DRF) 
y las vistas basadas en funciones para la renderización de la interfaz web.
"""
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

# Importación de modelos y serializadores del sistema.
from .models import Categoria, Insumo, Carro, CarroItem, Solicitud, SolicitudItem
from .serializers import CustomTokenObtainPairSerializer, CategoriaSerializer, InsumoSerializer, CarroItemSerializer

# ==========================================
# VISTAS DE LA API REST (BACKEND DRF)
# ==========================================

class CustomTokenObtainPairView(TokenObtainPairView):
    """ 
    Vista encargada de la generación de tokens JWT.
    Utiliza un serializador personalizado para inyectar roles de usuario.
    """
    serializer_class = CustomTokenObtainPairSerializer

class IsGestorBodega(permissions.BasePermission):
    """
    Clase de permiso personalizado (RBAC).
    Verifica que el usuario solicitante esté autenticado y posea el rol 'GESTOR'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'GESTOR'

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """ 
    Controlador para la consulta de categorías farmacéuticas.
    Restringido a usuarios autenticados.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticated]

class InsumoViewSet(viewsets.ModelViewSet):
    """
    Controlador principal del Catálogo de Insumos.
    Implementa filtrado dinámico mediante django-filter.
    """
    serializer_class = InsumoSerializer
    # Definición de campos disponibles para filtros estructurados.
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria', 'principio_activo']

    def get_queryset(self):
        """
        Sobrescritura del listado base:
        - Retorna el inventario completo (activos e inactivos) para perfiles Gestor.
        - Retorna únicamente los productos habilitados (activo=True) para perfiles Institución.
        """
        if self.request.user.is_authenticated and self.request.user.rol == 'GESTOR':
            return Insumo.objects.all().order_by('-id')
        return Insumo.objects.filter(activo=True).order_by('-id')

    def get_permissions(self):
        """ 
        Asignación dinámica de permisos según el método HTTP:
        Lectura abierta al público y modificación restringida a Gestores.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsGestorBodega()]

    def destroy(self, request, *args, **kwargs):
        """ 
        Sobrescritura del método DELETE para implementar borrado lógico.
        Marca el insumo como inactivo en lugar de eliminar la fila de la base de datos,
        protegiendo la integridad del historial de compras.
        """
        insumo = self.get_object()
        insumo.activo = False
        insumo.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarroViewSet(viewsets.ViewSet):
    """
    Controlador del Carro de Compras Persistente.
    Gestiona la lectura y modificación de ítems asociados a un usuario.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """ 
        Retorna la lista de productos asociados al carro activo del usuario solicitante. 
        Crea el carro si no existe previamente.
        """
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        items = CarroItem.objects.filter(carro=carro)
        serializer = CarroItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def agregar_insumo(self, request):
        """ 
        Adición de insumos al carro.
        Suma la cantidad solicitada si el ítem ya se encontraba presente en el carro.
        """
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        insumo_id = request.data.get('insumo')
        cantidad = int(request.data.get('cantidad', 1))
        
        insumo = Insumo.objects.get(id=insumo_id)
        item, created = CarroItem.objects.get_or_create(carro=carro, insumo=insumo, defaults={'cantidad': cantidad})
        if not created:
            item.cantidad += cantidad
            item.save()
        return Response({'status': 'Agregado al carro'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def eliminar_insumo(self, request, pk=None):
        """ 
        Eliminación de un insumo específico del carro de compras actual. 
        """
        try:
            item = CarroItem.objects.get(pk=pk, carro__usuario=request.user)
            item.delete()
            return Response({'status': 'Ítem eliminado'}, status=status.HTTP_204_NO_CONTENT)
        except CarroItem.DoesNotExist:
            return Response({'error': 'Ítem no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class TransaccionViewSet(viewsets.ViewSet):
    """
    Controlador de Órdenes y Transacciones atómicas.
    Maneja la liquidación del carro de compras y el descuento de inventario.
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def confirmar_solicitud(self, request):
        """
        Proceso de Checkout del Carro de Compras.
        Implementa transaction.atomic() para asegurar la consistencia transaccional:
        si ocurre un error de stock durante el bucle, la transacción completa es revertida.
        """
        try:
            with transaction.atomic():
                carro = Carro.objects.get(usuario=request.user)
                items_carro = CarroItem.objects.filter(carro=carro)
                
                if not items_carro.exists():
                    return Response({'error': 'Carro vacío'}, status=status.HTTP_400_BAD_REQUEST)

                # Generación de la orden en estado PAGADO.
                solicitud = Solicitud.objects.create(institucion=request.user, estado='PAGADO')

                for item in items_carro:
                    # Validación estricta de existencias físicas.
                    if item.insumo.stock < item.cantidad:
                        raise ValueError(f"Stock insuficiente para {item.insumo.nombre_comercial}")
                    
                    # Descuento atómico de inventario.
                    item.insumo.stock -= item.cantidad
                    item.insumo.save()

                    # Registro histórico del ítem con precio congelado.
                    SolicitudItem.objects.create(
                        solicitud=solicitud,
                        insumo=item.insumo,
                        cantidad=item.cantidad,
                        precio_congelado=item.insumo.precio_unitario
                    )
                
                # Eliminación de los ítems del carro tras confirmar la compra con éxito.
                items_carro.delete()
                return Response({'status': 'Solicitud confirmada'}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def mis_solicitudes(self, request):
        """ 
        Retorna el historial de compras y solicitudes de la Institución Médica en sesión. 
        """
        solicitudes = Solicitud.objects.filter(institucion=request.user).order_by('-fecha_creacion')
        data = [{
            'id': s.id,
            'estado': s.estado,
            'fecha_creacion': s.fecha_creacion,
            'items_count': s.items.count()
        } for s in solicitudes]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsGestorBodega])
    def todas_solicitudes(self, request):
        """ 
        Retorna todas las órdenes del sistema con detalle de ítems para el Gestor de Bodega. 
        """
        solicitudes = Solicitud.objects.all().order_by('-fecha_creacion')
        data = []
        for s in solicitudes:
            items_detalle = []
            total_cantidad = 0
            for item in s.items.all():
                items_detalle.append({
                    'insumo': item.insumo.nombre_comercial,
                    'cantidad': item.cantidad,
                    'precio_congelado': item.precio_congelado
                })
                total_cantidad += item.cantidad
                
            data.append({
                'id': s.id,
                'institucion': s.institucion.username,
                'estado': s.estado,
                'fecha_creacion': s.fecha_creacion,
                'items_count': total_cantidad,
                'detalle': items_detalle
            })
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsGestorBodega])
    def actualizar_estado(self, request, pk=None):
        """
        Actualización manual del estado de una orden.
        Si la orden es cancelada, se devuelven los insumos al stock físico de manera atómica.
        """
        solicitud = Solicitud.objects.get(pk=pk)
        nuevo_estado = request.data.get('estado')
        
        with transaction.atomic():
            if nuevo_estado == 'CANCELADO' and solicitud.estado != 'CANCELADO':
                for item in solicitud.items.all():
                    item.insumo.stock += item.cantidad
                    item.insumo.save()
            solicitud.estado = nuevo_estado
            solicitud.save()
            
        return Response({'status': 'Estado actualizado'})

# ==========================================
# VISTAS DEL FRONTEND (HTML / TEMPLATES)
# ==========================================

def home_view(request):
    """ Vista pública para renderizar el index o landing page. """
    return render(request, 'farmacia/index.html')

def custom_404_view(request, exception=None):
    """ Vista personalizada para renderizar errores de página no encontrada. """
    return render(request, 'farmacia/404.html', status=404)

def login_view(request):
    """ Vista para renderizar el formulario de autenticación JWT. """
    return render(request, 'farmacia/login.html')

def cliente_view(request):
    """ Vista del dashboard principal para las Instituciones Médicas. """
    return render(request, 'farmacia/cliente.html')

def gestor_view(request):
    """ Vista del dashboard administrativo para el Gestor de Bodega. """
    return render(request, 'farmacia/gestor.html')