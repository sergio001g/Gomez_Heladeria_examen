from django.db import models

class Sabor(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Producto(models.Model):
    sabor = models.ForeignKey(Sabor, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=50, unique=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    costo_insumos = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    class Meta:
        ordering = ['nombre']
