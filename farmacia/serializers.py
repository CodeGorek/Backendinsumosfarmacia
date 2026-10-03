"""
Módulo de serializadores de la aplicación farmacia.
Transforma los modelos de Django en formato JSON para la API REST,
y viceversa, validando las estructuras de datos entrantes y salientes.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Categoria, Insumo, Carro, CarroItem, Solicitud

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializador personalizado para la autenticación JWT.
    Permite la inyección del 'rol' del usuario dentro del payload (claims) del token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Inyección de claims personalizados para manejo de sesión y roles
        token['rol'] = user.rol
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

class CategoriaSerializer(serializers.ModelSerializer):
    """ Serializador para la exposición y lectura de las categorías farmacéuticas. """
    class Meta:
        model = Categoria
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    """ Serializador base para el manejo del catálogo de insumos médicos. """
    class Meta:
        model = Insumo
        fields = '__all__'

class CarroItemSerializer(serializers.ModelSerializer):
    """ Serializador para la gestión individual de los ítems en el carro de compras. """
    class Meta:
        model = CarroItem
        fields = ['id', 'insumo', 'cantidad']