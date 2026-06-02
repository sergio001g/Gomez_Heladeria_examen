from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SaborViewSet, ProductoViewSet, PedidoAPIView, ProduccionAPIView

router = DefaultRouter()
router.register(r"sabores", SaborViewSet, basename="sabores")
router.register(r"productos", ProductoViewSet, basename="productos")

urlpatterns = [
    path('pedido/', PedidoAPIView.as_view(), name='pedido'),
    path('produccion/', ProduccionAPIView.as_view(), name='produccion'),
]

urlpatterns += router.urls
