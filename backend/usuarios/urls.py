from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UsuarioViewSet, 
    PerfilDonoViewSet, 
    PerfilFuncionarioViewSet,
    CustomTokenObtainPairView
)

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')
router.register(r'donos', PerfilDonoViewSet, basename='perfilusuario')
router.register(r'funcionarios', PerfilFuncionarioViewSet, basename='perfilfuncionario')

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]