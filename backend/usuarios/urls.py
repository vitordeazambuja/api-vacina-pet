from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, PerfilDonoViewSet, PerfilFuncionarioViewSet

router = DefaultRouter()
router.register(r'users', UsuarioViewSet)
router.register(r'donos', PerfilDonoViewSet)
router.register(r'funcionarios', PerfilFuncionarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]