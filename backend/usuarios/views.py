from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario, PerfilDono, PerfilFuncionario
from .serializers import UsuarioSerializer, PerfilDonoSerializer, PerfilFuncionarioSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = Usuario.objects.get(username=request.data.get('username'))
            response.data['user'] = UsuarioSerializer(user).data
        return response


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class PerfilDonoViewSet(viewsets.ModelViewSet):
    queryset = PerfilDono.objects.all()
    serializer_class = PerfilDonoSerializer
    permission_classes = [IsAuthenticated]


class PerfilFuncionarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilFuncionario.objects.all()
    serializer_class = PerfilFuncionarioSerializer
    permission_classes = [IsAuthenticated]