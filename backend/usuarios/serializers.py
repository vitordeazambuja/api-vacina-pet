from rest_framework import serializers
from .models import Usuario, PerfilDono, PerfilFuncionario

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para criação e listagem de usuários.
    
    Campos:
    - id: Identificador único (somente leitura)
    - username: Nome de usuário único (obrigatório)
    - email: Email único (obrigatório)
    - password: Senha (somente escrita, nunca retorna)
    - is_staff: Se é funcionário/staff (padrão: False)
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'is_staff']

    def create(self, validated_data):
        """Cria novo usuário com senha criptografada"""
        user = Usuario.objects.create_user(**validated_data)
        return user

class PerfilDonoSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar perfis de donos (proprietários de pets).
    
    Campos:
    - id: Identificador único (somente leitura)
    - usuario: FK para usuário (obrigatório)
    - nome: Nome completo do dono (obrigatório)
    - cpf: CPF único (obrigatório)
    - endereco: Endereço completo (obrigatório)
    - telefone: Telefone de contato (obrigatório)
    - created_at: Data de criação (somente leitura)
    - updated_at: Data de atualização (somente leitura)
    """
    class Meta:
        model = PerfilDono
        fields = ['id', 'usuario', 'nome', 'cpf', 'endereco', 'telefone', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PerfilFuncionarioSerializer(serializers.ModelSerializer):
    """
    Serializer para gerenciar perfis de funcionários (veterinários/staff).
    
    Campos:
    - id: Identificador único (somente leitura)
    - usuario: FK para usuário (obrigatório)
    - nome: Nome completo (obrigatório)
    - cpf: CPF único (obrigatório)
    - endereco: Endereço (obrigatório)
    - telefone: Telefone de contato (obrigatório)
    - cargo: Cargo/função (ex: Veterinário, Técnico) (obrigatório)
    - created_at: Data de criação (somente leitura)
    - updated_at: Data de atualização (somente leitura)
    """
    class Meta:
        model = PerfilFuncionario
        fields = ['id', 'usuario', 'nome', 'cpf', 'endereco', 'telefone', 'cargo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']