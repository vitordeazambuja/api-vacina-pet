from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Pet, Vacina, PetVacina
from .serializers import PetSerializer, VacinaSerializer, PetVacinaSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

class VacinaViewSet(viewsets.ModelViewSet):
    queryset = Vacina.objects.all()
    serializer_class = VacinaSerializer
    permission_classes = [IsAuthenticated]

class PetVacinaViewSet(viewsets.ModelViewSet):
    queryset = PetVacina.objects.all()
    serializer_class = PetVacinaSerializer
    permission_classes = [IsAuthenticated]