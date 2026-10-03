"""
Módulo de Configuración del Panel de Administración de Django.
Registra y expone los modelos en la interfaz administrativa para la gestión
de cuentas B2B y visualización directa de la base de datos relacional.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Categoria, Insumo, Carro, CarroItem, Solicitud, SolicitudItem

class CustomUserAdmin(UserAdmin):
    """
    Configuración visual extendida para la entidad Usuario.
    Añade el campo 'rol' (Institución Médica o Gestor) a los formularios de creación 
    y edición, satisfaciendo la especificación de JWT y roles.
    """
    model = Usuario
    list_display = ['username', 'email', 'rol', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Configuración de Rol B2B', {'fields': ('rol',)}),
    )

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    """
    Configuración de la vista de inventario físico en el panel administrador.
    Habilita la búsqueda por texto y la segmentación rápida por categorías.
    """
    list_display = ('nombre_comercial', 'principio_activo', 'stock', 'precio_unitario', 'categoria')
    list_filter = ('categoria',)
    search_fields = ('nombre_comercial', 'principio_activo')

# Registro explícito de los modelos para su visibilidad en el panel
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Categoria)
admin.site.register(Carro)
admin.site.register(CarroItem)
admin.site.register(Solicitud)
admin.site.register(SolicitudItem)