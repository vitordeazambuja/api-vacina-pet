from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.username

class Perfil(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.PROTECT
    )
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome

class PerfilDono(Perfil):
    class Meta:
        db_table = 'perfil_dono'

class PerfilFuncionario(Perfil):
    cargo = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'perfil_funcionario'

    def __str__(self):
        return f"{self.nome} - {self.cargo}"