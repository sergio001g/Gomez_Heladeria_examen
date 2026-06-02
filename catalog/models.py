from django.db import models

class Plan(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Socio(models.Model):
    plan        = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="socios")
    nombre      = models.CharField(max_length=180)
    cedula      = models.CharField(max_length=20, unique=True)
    dias_atraso = models.IntegerField(default=0)
    activo      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"