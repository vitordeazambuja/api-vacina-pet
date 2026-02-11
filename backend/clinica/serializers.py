from rest_framework import serializers
from .models import Pet, Vacina, PetVacina

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = '__all__'

class PetVacinaSerializer(serializers.ModelSerializer):
    nome_vacina = serializers.SerializerMethodField()
    nome_pet = serializers.SerializerMethodField()

    class Meta:
        model = PetVacina
        fields = [
            'id', 'pet', 'nome_pet', 'vacina', 'nome_vacina', 
            'aplicador', 'data_aplicacao', 'proxima_dose', 'lote',
            'observacoes'
        ]

    def get_nome_vacina(self, obj):
        return obj.vacina.nome

    def get_nome_pet(self, obj):
        return obj.pet.nome