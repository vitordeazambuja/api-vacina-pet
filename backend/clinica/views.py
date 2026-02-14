from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
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

    @action(detail=True, methods=['get'])
    def historico_vacinas(self, request, pk=None):
        pet = self.get_object()
        self._validar_acesso_pet(request.user, pet)
        
        historico = pet.historico_vacinas.all().order_by('-data_aplicacao')
        serializer = PetVacinaSerializer(historico, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def proximas_doses(self, request, pk=None):
        pet = self.get_object()
        self._validar_acesso_pet(request.user, pet)
        
        proximas = pet.obter_proximas_doses()
        return Response({
            'pet_id': pet.id,
            'pet_nome': pet.nome,
            'proximas_doses': proximas
        })

    @action(detail=True, methods=['get'])
    def doses_vencidas(self, request, pk=None):
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

    @action(detail=False, methods=['get'])
    def proximas_doses_sistema(self, request):
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

    @action(detail=False, methods=['get'])
    def doses_vencidas_sistema(self, request):
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