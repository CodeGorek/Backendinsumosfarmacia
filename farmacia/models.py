"""
Módulo de Modelos de la aplicación Farmacia.
Definición estructural de la base de datos PostgreSQL utilizando el ORM de Django.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado.
    Extiende AbstractUser de Django para habilitar la asignación de roles de negocio B2B.
    """
    # Restricción de roles según la matriz de acceso B2B
    ROLE_CHOICES = (
        ('INSTITUCION', 'Institución Médica'),
        ('GESTOR', 'Gestor de Bodega'),
    )
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='INSTITUCION')

class Categoria(models.Model):
    """ Entidad para clasificar los productos médicos dentro del catálogo. """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    """
    Entidad del Insumo Médico.
    Maneja la información comercial del producto, existencias físicas y valor comercial.
    """
    nombre_comercial = models.CharField(max_length=200)
    principio_activo = models.CharField(max_length=200)
    lote = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='insumos')
    activo = models.BooleanField(default=True)
    # Permite la inserción de rutas relativas locales o hipervínculos externos
    imagen_url = models.CharField(max_length=800, blank=True, null=True, default='/static/farmacia/img/default.jpg')

class Carro(models.Model):
    """
    Entidad del Carro de Compras Persistente.
    Obligatoriedad de Relación 1 a 1 con Usuario para garantizar la persistencia post-logout.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='carro')
    creado_en = models.DateTimeField(auto_now_add=True)

class CarroItem(models.Model):
    """ Detalle transaccional de un insumo temporal dentro de un carro de compras activo. """
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE, related_name='items')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class Solicitud(models.Model):
    """
    Entidad de Solicitud u Orden de Compra.
    Actúa como cabecera del historial de compras finalizadas por un cliente.
    """
    # Definición de enumeraciones explícitas para el seguimiento de la orden
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    )
    institucion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class SolicitudItem(models.Model):
    """
    Detalle inmutable de una orden procesada.
    Congela el valor comercial exacto que tenía el insumo al momento de la liquidación.
    """
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='items')
    insumo = models.ForeignKey(Insumo, on_delete=models.RESTRICT)
    cantidad = models.PositiveIntegerField()
    precio_congelado = models.DecimalField(max_digits=10, decimal_places=2)