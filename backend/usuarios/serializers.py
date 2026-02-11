from rest_framework import serializers
from .models import Usuario, PerfilDono, PerfilFuncionario

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'is_staff']

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user

class PerfilDonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilDono
        fields = '__all__'

class PerfilFuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilFuncionario
        fields = '__all__'