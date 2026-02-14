from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, 
    PerfilDonoViewSet, 
    PerfilFuncionarioViewSet,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfis-donos', PerfilDonoViewSet, basename='perfilusuario')
router.register(r'perfis-funcionarios', PerfilFuncionarioViewSet, basename='perfilfuncionario')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]