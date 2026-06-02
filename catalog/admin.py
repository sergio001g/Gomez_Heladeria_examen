from django.contrib import admin
from .models import Sabor, Producto

@admin.register(Sabor)
class SaborAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'producto_count']
    search_fields = ['nombre']

    def producto_count(self, obj):
        return obj.productos.count()
    producto_count.short_description = 'Productos'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'sabor', 'precio_venta', 'costo_insumos', 'disponible']
    list_filter = ['sabor', 'disponible']
    search_fields = ['nombre', 'codigo']
    readonly_fields = ['id']

