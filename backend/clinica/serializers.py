from rest_framework import serializers
from .models import Pet, Vacina, PetVacina

class PetSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar pets com informações completas de vacinação.
    
    Campos:
    - id: Identificador único (somente leitura)
    - dono: FK para PerfilDono (somente leitura, auto-preenchido com o usuário logado)
    - nome: Nome do pet (obrigatório)
    - especie: Ex: Cachorro, Gato (obrigatório)
    - raca: Raça/tipo (obrigatório)
    - peso: Peso em kg (obrigatório, mínimo 0.01)
    - data_nascimento: Data de nascimento (opcional)
    - idade_anos: Calculada automaticamente (somente leitura)
    - idade_dias: Calculada automaticamente (somente leitura)
    - proximas_doses: Lista de próximas vacinas (somente leitura)
    - doses_vencidas: Lista de vacinas atrasadas (somente leitura)
    - nome_dono: Nome do dono (somente leitura)
    - created_at: Data de criação (somente leitura)
    - updated_at: Data de atualização (somente leitura)
    """
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
        read_only_fields = ['id', 'dono', 'created_at', 'updated_at']
    
    def get_idade_anos(self, obj):
        """Calcula idade em anos baseado na data de nascimento"""
        return obj.calcular_idade_anos()

    def get_idade_dias(self, obj):
        """Calcula idade em dias baseado na data de nascimento"""
        return obj.calcular_idade_dias()

    def get_proximas_doses(self, obj):
        """Retorna lista de próximas doses não vencidas"""
        return obj.obter_proximas_doses()

    def get_doses_vencidas(self, obj):
        """Retorna lista de doses em atraso"""
        return obj.obter_doses_vencidas()

class VacinaSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar o catálogo de vacinas disponíveis.
    
    Campos:
    - id: Identificador único (somente leitura)
    - nome: Nome da vacina (ex: Raiva, Polivalente) (obrigatório)
    - fabricante: Laboratório/fabricante (obrigatório)
    - valor: Preço em R$ (obrigatório, mínimo 0.01)
    - intervalo_doses_dias: Dias entre doses (obrigatório, ex: 365)
    - descricao: Descrição detalhada (obrigatório)
    - created_at: Data de criação (somente leitura)
    - updated_at: Data de atualização (somente leitura)
    
    Nota: Apenas funcionários podem criar/editar/deletar vacinas
    """
    class Meta:
        model = Vacina
        fields = [
            'id', 'nome', 'fabricante', 'valor', 
            'intervalo_doses_dias', 'descricao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PetVacinaSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar registros de vacinação aplicadas a pets.
    
    Campos:
    - id: Identificador único (somente leitura)
    - pet: FK para Pet (obrigatório)
    - nome_pet: Nome do pet (somente leitura)
    - vacina: FK para Vacina (obrigatório)
    - nome_vacina: Nome da vacina (somente leitura)
    - aplicador: FK para PerfilFuncionario (obrigatório)
    - nome_aplicador: Nome do veterinário (somente leitura)
    - data_aplicacao: Data da aplicação (obrigatório, formato: YYYY-MM-DD)
    - proxima_dose: Data próxima dose (calculada automaticamente)
    - lote: Lote da vacina (obrigatório)
    - observacoes: Notas adicionais (opcional)
    - esta_vencida: Se está vencida (somente leitura)
    - status: Status automático (somente leitura)
        - 'em_dia': Próxima dose > 7 dias
        - 'proxima_em_breve': Próxima dose em até 7 dias
        - 'vencida': Próxima dose passou
        - 'indefinido': Sem próxima dose
    - created_at: Data de criação (somente leitura)
    - updated_at: Data de atualização (somente leitura)
    
    Nota: Apenas funcionários podem criar/editar/deletar registros
    Nota: Próxima dose é calculada automaticamente = data_aplicacao + vacina.intervalo_doses_dias
    """
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
        """Verifica se a próxima dose está vencida"""
        return obj.esta_vencida()

    def get_status(self, obj):
        """Retorna o status automático da vacinação"""
        return obj.get_status()