from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, SocioViewSet

router = DefaultRouter()
router.register(r"planes", PlanViewSet,  basename="planes")
router.register(r"socios", SocioViewSet, basename="socios")

urlpatterns = []
urlpatterns += router.urls