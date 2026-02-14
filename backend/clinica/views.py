from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from datetime import date

from .models import Pet, Vacina, PetVacina
from .serializers import PetSerializer, VacinaSerializer, PetVacinaSerializer
from usuarios.models import PerfilDono


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            queryset = Pet.objects.all()
            dono_id = self.request.query_params.get('dono_id') # type: ignore
            if dono_id:
                queryset = queryset.filter(dono_id=dono_id)
            return queryset
        
        try:
            dono = PerfilDono.objects.get(usuario=user)
            return Pet.objects.filter(dono=dono)
        except PerfilDono.DoesNotExist:
            return Pet.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        
        if 'dono' not in serializer.initial_data:
            dono = self._obter_dono_usuario(user)
            serializer.save(dono=dono)
        else:
            if not user.is_staff:
                dono = self._obter_dono_usuario(user)
                if int(serializer.initial_data['dono']) != dono.id: # type: ignore
                    raise PermissionDenied("Você pode apenas criar pets para si mesmo.")
            serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        pet = self.get_object()
        
        if not user.is_staff:
            dono = self._obter_dono_usuario(user)
            if pet.dono != dono:
                raise PermissionDenied("Você pode apenas editar seus próprios pets.")
        
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        
        if not user.is_staff:
            dono = self._obter_dono_usuario(user)
            if instance.dono != dono:
                raise PermissionDenied("Você pode apenas deletar seus próprios pets.")
        
        instance.delete()
    
    def _obter_dono_usuario(self, user):
        try:
            return PerfilDono.objects.get(usuario=user)
        except PerfilDono.DoesNotExist:
            raise PermissionDenied("Usuário não possui um perfil de dono.")

    @extend_schema(
        tags=['Pets'],
        summary='Listar pets',
        description='Lista todos os pets. Donos veem apenas seus pets, funcionários veem todos.',
        parameters=[
            OpenApiParameter(
                name='dono_id',
                type=int,
                description='Filtrar pets por ID do dono (apenas para staff)',
                required=False
            )
        ],
        examples=[
            OpenApiExample(
                'Resposta - Sucesso',
                value=[
                    {
                        'id': 1,
                        'dono': 5,
                        'nome_dono': 'João Silva',
                        'nome': 'Rex',
                        'especie': 'Cachorro',
                        'raca': 'Labrador',
                        'peso': '35.50',
                        'data_nascimento': '2020-05-15',
                        'idade_anos': 3,
                        'idade_dias': 1370,
                        'proximas_doses': [
                            {
                                'vacina': 'Raiva',
                                'data_proxima_dose': '2025-03-15',
                                'dias_restantes': 30
                            }
                        ],
                        'doses_vencidas': []
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets'],
        summary='Criar novo pet',
        description='Cria um novo pet. Donos são automaticamente definidos. Funcionários podem registrar pets para outros donos.',
        examples=[
            OpenApiExample(
                'Requisição - Dono criando seu pet',
                value={
                    'nome': 'Miau',
                    'especie': 'Gato',
                    'raca': 'Persa',
                    'peso': '4.50',
                    'data_nascimento': '2022-01-10'
                }
            ),
            OpenApiExample(
                'Resposta',
                value={
                    'id': 1,
                    'dono': 5,
                    'nome_dono': 'Maria Silva',
                    'nome': 'Miau',
                    'especie': 'Gato',
                    'raca': 'Persa',
                    'peso': '4.50',
                    'data_nascimento': '2022-01-10',
                    'idade_anos': 2,
                    'idade_dias': 790,
                    'created_at': '2025-02-13T10:30:45Z'
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets'],
        summary='Obter detalhes do pet',
        description='Retorna informações completas de um pet, incluindo histórico de vacinação'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets'],
        summary='Atualizar pet',
        description='Atualiza informações de um pet. Donos podem editar apenas seus pets, funcionários podem editar qualquer pet.'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets'],
        summary='Atualizar parcialmente um pet',
        description='Atualiza apenas campos específicos de um pet (PATCH). Donos só podem editar seus pets.'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets'],
        summary='Deletar pet',
        description='Remove um pet do sistema. Donos podem deletar apenas seus pets, funcionários podem deletar qualquer pet.'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        tags=['Pets - Vacinação'],
        summary='Histórico de vacinação',
        description='Lista todas as vacinas aplicadas a um pet, com status e próximas doses',
        examples=[
            OpenApiExample(
                'Resposta',
                value=[
                    {
                        'id': 1,
                        'pet': 1,
                        'nome_pet': 'Rex',
                        'vacina': 10,
                        'nome_vacina': 'Raiva',
                        'aplicador': 3,
                        'nome_aplicador': 'Dr. João',
                        'data_aplicacao': '2025-01-15',
                        'proxima_dose': '2026-01-15',
                        'lote': 'RAIVA-2025-001',
                        'observacoes': 'Sem reações',
                        'esta_vencida': False,
                        'status': 'em_dia'
                    }
                ]
            )
        ]
    )
    @action(detail=True, methods=['get'])
    def historico_vacinas(self, request, pk=None):
        """Retorna o histórico completo de vacinação do pet"""
        pet = self.get_object()
        self._validar_acesso_pet(request.user, pet)
        
        historico = pet.historico_vacinas.all().order_by('-data_aplicacao')
        serializer = PetVacinaSerializer(historico, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Pets - Vacinação'],
        summary='Próximas doses agendadas',
        description='Lista todas as próximas doses de vacina do pet com data e dias restantes',
        examples=[
            OpenApiExample(
                'Resposta',
                value={
                    'pet_id': 1,
                    'pet_nome': 'Rex',
                    'proximas_doses': [
                        {
                            'vacina': 'Raiva',
                            'data_proxima_dose': '2025-03-15',
                            'dias_restantes': 30,
                            'historico_id': 1
                        },
                        {
                            'vacina': 'Polivalente',
                            'data_proxima_dose': '2025-04-20',
                            'dias_restantes': 66,
                            'historico_id': 2
                        }
                    ]
                }
            )
        ]
    )
    @action(detail=True, methods=['get'])
    def proximas_doses(self, request, pk=None):
        """Retorna apenas as próximas doses não vencidas"""
        pet = self.get_object()
        self._validar_acesso_pet(request.user, pet)
        
        proximas = pet.obter_proximas_doses()
        return Response({
            'pet_id': pet.id,
            'pet_nome': pet.nome,
            'proximas_doses': proximas
        })

    @extend_schema(
        tags=['Pets - Vacinação'],
        summary='Doses de vacina vencidas',
        description='Lista todas as doses em atraso que precisam ser aplicadas',
        examples=[
            OpenApiExample(
                'Resposta',
                value={
                    'pet_id': 1,
                    'pet_nome': 'Zara',
                    'doses_vencidas': [
                        {
                            'vacina': 'Polivalente',
                            'data_proxima_dose': '2024-12-20',
                            'dias_vencido': 85,
                            'historico_id': 5
                        }
                    ]
                }
            )
        ]
    )
    @action(detail=True, methods=['get'])
    def doses_vencidas(self, request, pk=None):
        """Retorna apenas as doses vencidas"""
        pet = self.get_object()
        self._validar_acesso_pet(request.user, pet)
        
        vencidas = pet.obter_doses_vencidas()
        return Response({
            'pet_id': pet.id,
            'pet_nome': pet.nome,
            'doses_vencidas': vencidas
        })
    
    def _validar_acesso_pet(self, user, pet):
        if not user.is_staff:
            dono = self._obter_dono_usuario(user)
            if pet.dono != dono:
                raise PermissionDenied("Você pode apenas acessar seus próprios pets.")


class VacinaViewSet(viewsets.ModelViewSet):
    queryset = Vacina.objects.all()
    serializer_class = VacinaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self._validar_staff()
        serializer.save()

    def perform_update(self, serializer):
        self._validar_staff()
        serializer.save()

    def perform_destroy(self, instance):
        self._validar_staff()
        instance.delete()
    
    def _validar_staff(self):
        if not self.request.user.is_staff:
            raise PermissionDenied("Apenas funcionários podem realizar esta ação.")

    @extend_schema(
        tags=['Vacinas'],
        summary='Listar vacinas disponíveis',
        description='Lista todas as vacinas cadastradas no sistema. Apenas leitura para todos os usuários.',
        examples=[
            OpenApiExample(
                'Resposta',
                value=[
                    {
                        'id': 1,
                        'nome': 'Raiva',
                        'fabricante': 'Boehringer Ingelheim',
                        'valor': '85.00',
                        'intervalo_doses_dias': 365,
                        'descricao': 'Vacina contra raiva. Recomendada anualmente.'
                    },
                    {
                        'id': 2,
                        'nome': 'Polivalente',
                        'fabricante': 'Intervet',
                        'valor': '120.00',
                        'intervalo_doses_dias': 365,
                        'descricao': 'Vacina polivalente para cães. Protege contra múltiplas doenças.'
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Vacinas'],
        summary='Criar nova vacina',
        description='Cria uma nova vacina no sistema. Apenas funcionários podem realizar esta ação.',
        examples=[
            OpenApiExample(
                'Requisição',
                value={
                    'nome': 'Raiva',
                    'fabricante': 'Boehringer Ingelheim',
                    'valor': '85.00',
                    'intervalo_doses_dias': 365,
                    'descricao': 'Vacina contra raiva. Recomendada anualmente para cães e gatos.'
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Vacinas'],
        summary='Obter detalhes da vacina',
        description='Retorna informações completas de uma vacina cadastrada'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Vacinas'],
        summary='Atualizar vacina',
        description='Atualiza informações de uma vacina. Apenas funcionários podem modificar vacinas.'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Vacinas'],
        summary='Atualizar parcialmente uma vacina',
        description='Atualiza apenas campos específicos de uma vacina (PATCH). Apenas funcionários.'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Vacinas'],
        summary='Deletar vacina',
        description='Remove uma vacina do sistema. Apenas funcionários podem deletar vacinas.'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PetVacinaViewSet(viewsets.ModelViewSet):
    serializer_class = PetVacinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return PetVacina.objects.all()
        
        try:
            dono = PerfilDono.objects.get(usuario=user)
            return PetVacina.objects.filter(pet__dono=dono)
        except PerfilDono.DoesNotExist:
            return PetVacina.objects.none()

    def perform_create(self, serializer):
        self._validar_staff()
        serializer.save()

    def perform_update(self, serializer):
        self._validar_staff()
        serializer.save()

    def perform_destroy(self, instance):
        self._validar_staff()
        instance.delete()
    
    def _validar_staff(self):
        if not self.request.user.is_staff:
            raise PermissionDenied("Apenas funcionários podem realizar esta ação.")

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Listar registros de vacinação',
        description='Lista todos os registros de vacinação. Donos veem apenas seus pets, funcionários veem todos.',
        examples=[
            OpenApiExample(
                'Resposta',
                value=[
                    {
                        'id': 1,
                        'pet': 1,
                        'nome_pet': 'Rex',
                        'vacina': 10,
                        'nome_vacina': 'Raiva',
                        'aplicador': 3,
                        'nome_aplicador': 'Dr. João Santos',
                        'data_aplicacao': '2025-01-15',
                        'proxima_dose': '2026-01-15',
                        'lote': 'RAIVA-2025-001',
                        'observacoes': 'Sem reações adversas',
                        'esta_vencida': False,
                        'status': 'em_dia'
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Registrar vacinação',
        description='''Registra uma nova aplicação de vacina. Apenas funcionários podem registrar.
        A próxima dose é calculada automaticamente baseada no intervalo definido para a vacina.
        Status automático: "em_dia" (padrão), "próxima_em_breve" (até 7 dias), "vencida" (ultrapassou data).''',
        examples=[
            OpenApiExample(
                'Requisição',
                value={
                    'pet': 1,
                    'vacina': 10,
                    'aplicador': 3,
                    'data_aplicacao': '2025-02-13',
                    'lote': 'RAIVA-2025-001',
                    'observacoes': 'Animal com boa saúde, sem reações'
                }
            ),
            OpenApiExample(
                'Resposta',
                value={
                    'id': 1,
                    'pet': 1,
                    'nome_pet': 'Rex',
                    'vacina': 10,
                    'nome_vacina': 'Raiva',
                    'aplicador': 3,
                    'nome_aplicador': 'Dr. João',
                    'data_aplicacao': '2025-02-13',
                    'proxima_dose': '2026-02-13',
                    'lote': 'RAIVA-2025-001',
                    'observacoes': 'Animal com boa saúde, sem reações',
                    'status': 'em_dia'
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Obter detalhes da vacinação',
        description='Retorna informações completas de um registro de vacinação'
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Atualizar registro de vacinação',
        description='Atualiza informações de um registro de vacinação. Apenas funcionários podem modificar.'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Atualizar parcialmente um registro',
        description='Atualiza apenas campos específicos de um registro de vacinação (PATCH). Apenas funcionários.'
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Histórico de Vacinação'],
        summary='Deletar registro de vacinação',
        description='Remove um registro de vacinação do sistema. Apenas funcionários podem deletar.'
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        tags=['Relatórios - Staff'],
        summary='Próximas doses do sistema',
        description='Listagem de todas as próximas doses agendadas para todos os pets no sistema. Apenas funcionários.',
        examples=[
            OpenApiExample(
                'Resposta',
                value={
                    'total': 5,
                    'proximas_doses': [
                        {
                            'pet_id': 1,
                            'pet_nome': 'Rex',
                            'dono': 'João Silva',
                            'vacina': 'Raiva',
                            'proxima_dose': '2025-03-15',
                            'dias_restantes': 30
                        },
                        {
                            'pet_id': 2,
                            'pet_nome': 'Miau',
                            'dono': 'Maria Santos',
                            'vacina': 'Polivalente',
                            'proxima_dose': '2025-03-20',
                            'dias_restantes': 35
                        }
                    ]
                }
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def proximas_doses_sistema(self, request):
        """Relatório administrativo de próximas doses"""
        self._validar_staff()
        
        proximas = []
        for pet_vacina in PetVacina.objects.filter(
            proxima_dose__isnull=False
        ).order_by('proxima_dose'):
            if not pet_vacina.esta_vencida():
                dias = (pet_vacina.proxima_dose - date.today()).days # type: ignore
                proximas.append({
                    'pet_id': pet_vacina.pet.id, # type: ignore
                    'pet_nome': pet_vacina.pet.nome,
                    'dono': pet_vacina.pet.dono.nome,
                    'vacina': pet_vacina.vacina.nome,
                    'proxima_dose': pet_vacina.proxima_dose,
                    'dias_restantes': dias
                })
        
        return Response({
            'total': len(proximas),
            'proximas_doses': proximas
        })

    @extend_schema(
        tags=['Relatórios - Staff'],
        summary='Doses vencidas do sistema',
        description='Listagem de todas as doses em atraso que precisam de nova aplicação. Apenas funcionários.',
        examples=[
            OpenApiExample(
                'Resposta',
                value={
                    'total': 2,
                    'doses_vencidas': [
                        {
                            'pet_id': 3,
                            'pet_nome': 'Zara',
                            'dono': 'Pedro Costa',
                            'vacina': 'Polivalente',
                            'proxima_dose_era': '2024-12-20',
                            'dias_vencido': 85
                        }
                    ]
                }
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def doses_vencidas_sistema(self, request):
        """Relatório administrativo de doses vencidas"""
        self._validar_staff()
        
        vencidas = []
        for pet_vacina in PetVacina.objects.filter(
            proxima_dose__isnull=False
        ).order_by('proxima_dose'):
            if pet_vacina.esta_vencida():
                dias = (date.today() - pet_vacina.proxima_dose).days # type: ignore
                vencidas.append({
                    'pet_id': pet_vacina.pet.id, # type: ignore
                    'pet_nome': pet_vacina.pet.nome,
                    'dono': pet_vacina.pet.dono.nome,
                    'vacina': pet_vacina.vacina.nome,
                    'proxima_dose_era': pet_vacina.proxima_dose,
                    'dias_vencido': dias
                })
        
        return Response({
            'total': len(vencidas),
            'doses_vencidas': vencidas
        })