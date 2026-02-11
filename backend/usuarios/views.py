from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Usuario, PerfilDono, PerfilFuncionario
from .serializers import UsuarioSerializer, PerfilDonoSerializer, PerfilFuncionarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class PerfilDonoViewSet(viewsets.ModelViewSet):
    queryset = PerfilDono.objects.all()
    serializer_class = PerfilDonoSerializer
    permission_classes = [IsAuthenticated]

class PerfilFuncionarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilFuncionario.objects.all()
    serializer_class = PerfilFuncionarioSerializer
    permission_classes = [IsAuthenticated]