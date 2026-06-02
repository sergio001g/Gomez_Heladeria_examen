from rest_framework import serializers
from .models import Plan, Socio

class PlanSerializer(serializers.ModelSerializer):
    total_socios = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Plan
        fields = ["id", "nombre", "precio", "activo", "total_socios"]

    def get_total_socios(self, obj):
        return obj.socios.filter(activo=True).count()

class SocioSerializer(serializers.ModelSerializer):
    plan_nombre = serializers.CharField(source="plan.nombre", read_only=True)

    class Meta:
        model  = Socio
        fields = ["id", "plan", "plan_nombre", "nombre", "cedula",
                  "dias_atraso", "activo", "creado_en"]