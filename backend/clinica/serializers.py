from rest_framework import serializers
from .models import Pet, Vacina, PetVacina

class PetSerializer(serializers.ModelSerializer):
    idade_anos = serializers.SerializerMethodField()
    idade_dias = serializers.SerializerMethodField()
    proximas_doses = serializers.SerializerMethodField()
    doses_vencidas = serializers.SerializerMethodField()
    nome_dono = serializers.CharField(source='dono.nome', read_only=True)

    class Meta:
        model = Pet
        fields = [
            'id', 'dono', 'nome_dono', 'nome', 'especie', 'raca', 
            'peso', 'data_nascimento', 'idade_anos', 'idade_dias',
            'proximas_doses', 'doses_vencidas', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_idade_anos(self, obj):
        return obj.calcular_idade_anos()

    def get_idade_dias(self, obj):
        return obj.calcular_idade_dias()

    def get_proximas_doses(self, obj):
        return obj.obter_proximas_doses()

    def get_doses_vencidas(self, obj):
        return obj.obter_doses_vencidas()

class VacinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacina
        fields = [
            'id', 'nome', 'fabricante', 'valor', 
            'intervalo_doses_dias', 'descricao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PetVacinaSerializer(serializers.ModelSerializer):
    nome_vacina = serializers.CharField(source='vacina.nome', read_only=True)
    nome_pet = serializers.CharField(source='pet.nome', read_only=True)
    nome_aplicador = serializers.CharField(source='aplicador.nome', read_only=True)
    esta_vencida = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = PetVacina
        fields = [
            'id', 'pet', 'nome_pet', 'vacina', 'nome_vacina', 
            'aplicador', 'nome_aplicador', 'data_aplicacao', 
            'proxima_dose', 'lote', 'observacoes', 'esta_vencida',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'proxima_dose', 'created_at', 'updated_at', 'esta_vencida', 'status']

    def get_esta_vencida(self, obj):
        return obj.esta_vencida()

    def get_status(self, obj):
        return obj.get_status()