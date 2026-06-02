from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from .models import Sabor, Producto
from .serializers import SaborSerializer, SaborDetailSerializer, ProductoSerializer
from .permissions import IsAdminOrReadOnly

class SaborViewSet(viewsets.ModelViewSet):
    queryset = Sabor.objects.all().order_by('nombre')
    serializer_class = SaborSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SaborDetailSerializer
        return SaborSerializer

    def perform_destroy(self, instance):
        if instance.productos.exists():
            return Response(
                {'error': 'No se puede eliminar un sabor que tiene productos asociados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.select_related('sabor').all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sabor', 'disponible']
    search_fields = ['nombre', 'codigo']
    ordering_fields = ['nombre', 'codigo', 'precio_venta', 'id']

class PedidoAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        items = request.data

        if not isinstance(items, list):
            return Response(
                {'error': 'El body debe ser una lista de items'},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_unidades = 0
        subtotal = 0
        detalle = []

        for item in items:
            nombre = item.get('nombre', '')
            precio = float(item.get('precio', 0))
            cantidad = int(item.get('cantidad', 0))

            subtotal_linea = precio * cantidad
            subtotal += subtotal_linea
            total_unidades += cantidad

            detalle.append({
                'nombre': nombre,
                'cantidad': cantidad,
                'subtotal_linea': subtotal_linea
            })

        if total_unidades <= 3:
            descuento_pct = 0
        elif total_unidades <= 6:
            descuento_pct = 10
        elif total_unidades <= 10:
            descuento_pct = 15
        else:
            descuento_pct = 20

        descuento = subtotal * (descuento_pct / 100)
        total = subtotal - descuento

        return Response({
            'total_unidades': total_unidades,
            'subtotal': round(subtotal, 2),
            'descuento_pct': descuento_pct,
            'total': round(total, 2),
            'detalle': detalle
        }, status=status.HTTP_200_OK)

class ProduccionAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        presupuesto = float(request.query_params.get('presupuesto', 0))
        costos_str = request.query_params.get('costos', '')

        if not costos_str:
            return Response(
                {'error': 'El parámetro costos es obligatorio'},
                status=status.HTTP_400_BAD_REQUEST
            )

        costos = [float(c.strip()) for c in costos_str.split(',')]

        acumulado = 0
        indice = 0
        productos_producidos = 0
        detalle = []

        while indice < len(costos):
            costo_actual = costos[indice]

            if acumulado + costo_actual <= presupuesto:
                acumulado += costo_actual
                productos_producidos += 1
                detalle.append({
                    'producto_numero': productos_producidos,
                    'costo': round(costo_actual, 2)
                })
                indice += 1
            else:
                break

        presupuesto_restante = presupuesto - acumulado

        return Response({
            'productos_producidos': productos_producidos,
            'presupuesto_gastado': round(acumulado, 2),
            'presupuesto_restante': round(presupuesto_restante, 2),
            'detalle': detalle
        }, status=status.HTTP_200_OK)
