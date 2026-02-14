from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
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

    @extend_schema(
        tags=['Autenticação'],
        summary='Gerar token de acesso',
        description='Autentica o usuário com credenciais e retorna tokens JWT (access e refresh)',
        examples=[
            OpenApiExample(
                'Requisição',
                value={
                    'username': 'joao_silva',
                    'password': 'senha123'
                }
            ),
            OpenApiExample(
                'Resposta',
                value={
                    'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
                    'user': {
                        'id': 1,
                        'username': 'joao_silva',
                        'email': 'joao@example.com',
                        'is_staff': False
                    }
                }
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = Usuario.objects.get(username=request.data.get('username'))
            response.data['user'] = UsuarioSerializer(user).data
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    View customizada para renovar token JWT com documentação Swagger
    """
    @extend_schema(
        tags=['Autenticação'],
        summary='Renovar token de acesso',
        description='Usa o refresh token (válido por 24h) para obter um novo access token (válido por 15min) sem fazer login novamente',
        examples=[
            OpenApiExample(
                'Requisição',
                value={
                    'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                }
            ),
            OpenApiExample(
                'Resposta',
                value={
                    'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
                }
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(
        tags=['Autenticação'],
        summary='Registrar novo usuário',
        description='Cria uma nova conta de usuário. Sem autenticação necessária.',
        examples=[
            OpenApiExample(
                'Requisição',
                value={
                    'username': 'joao_silva',
                    'email': 'joao@example.com',
                    'password': 'senha123',
                    'is_staff': False
                }
            ),
            OpenApiExample(
                'Resposta',
                value={
                    'id': 1,
                    'username': 'joao_silva',
                    'email': 'joao@example.com',
                    'is_staff': False
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Autenticação'],
        summary='Listar usuários',
        description='Lista todos os usuários cadastrados. Apenas staff pode visualizar.',
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Autenticação'],
        summary='Obter dados do usuário logado',
        description='Retorna as informações do usuário autenticado no token JWT',
        examples=[
            OpenApiExample(
                'Resposta',
                value={
                    'id': 1,
                    'username': 'joao_silva',
                    'email': 'joao@example.com',
                    'is_staff': False
                }
            )
        ]
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Retorna o perfil do usuário autenticado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        tags=['Usuários'],
        summary='Obter detalhes do usuário',
        description='Retorna informações completas de um usuário por ID. Apenas staff pode visualizar outros usuários.'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Usuários'],
        summary='Atualizar usuário',
        description='Atualiza informações de um usuário. Cada usuário pode atualizar apenas sua própria conta.'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Usuários'],
        summary='Atualizar parcialmente um usuário',
        description='Atualiza apenas campos específicos de um usuário (PATCH). Cada usuário pode atualizar apenas sua própria conta.'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Usuários'],
        summary='Deletar usuário',
        description='Remove uma conta de usuário do sistema.'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PerfilDonoViewSet(viewsets.ModelViewSet):
    queryset = PerfilDono.objects.all()
    serializer_class = PerfilDonoSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Listar perfis de donos',
        description='Lista todos os perfis de donos de pets registrados'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Criar perfil de dono',
        description='Cria um perfil de dono de pet. Um usuário pode ter apenas um perfil de dono.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Obter perfil de dono',
        description='Retorna informações do perfil de um dono'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Atualizar perfil de dono',
        description='Atualiza informações do perfil de um dono'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Atualizar parcialmente perfil de dono',
        description='Atualiza apenas campos específicos do perfil de um dono (PATCH)'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Dono'],
        summary='Deletar perfil de dono',
        description='Remove um perfil de dono do sistema'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PerfilFuncionarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilFuncionario.objects.all()
    serializer_class = PerfilFuncionarioSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Listar perfis de funcionários',
        description='Lista todos os perfis de funcionários registrados'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Criar perfil de funcionário',
        description='Cria um perfil de funcionário. Apenas staff pode criar funcionários.',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Obter perfil de funcionário',
        description='Retorna informações do perfil de um funcionário'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Atualizar perfil de funcionário',
        description='Atualiza informações do perfil de um funcionário'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Atualizar parcialmente perfil de funcionário',
        description='Atualiza apenas campos específicos do perfil de um funcionário (PATCH)'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Perfis - Funcionário'],
        summary='Deletar perfil de funcionário',
        description='Remove um perfil de funcionário do sistema'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)