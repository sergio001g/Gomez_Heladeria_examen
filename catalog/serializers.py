from rest_framework import serializers
from .models import Sabor, Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'sabor', 'nombre', 'codigo', 'precio_venta', 'costo_insumos', 'disponible']

class SaborSerializer(serializers.ModelSerializer):
    total_productos = serializers.SerializerMethodField()

    class Meta:
        model = Sabor
        fields = ['id', 'nombre', 'total_productos']

    def get_total_productos(self, obj):
        return obj.productos.filter(disponible=True).count()

class SaborDetailSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)
    total_productos = serializers.SerializerMethodField()

    class Meta:
        model = Sabor
        fields = ['id', 'nombre', 'total_productos', 'productos']

    def get_total_productos(self, obj):
        return obj.productos.filter(disponible=True).count()
