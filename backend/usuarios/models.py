from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo customizado de usuário que estende o AbstractUser do Django.
    
    Campos adicionais:
    - created_at: Data de criação da conta
    - updated_at: Data de última atualização
    
    Campos herdados:
    - id, username, email, password, is_staff, is_superuser, is_active, etc
    
    Tipos de usuário:
    - is_staff=False: Dono de pets (usuário comum)
    - is_staff=True: Funcionário/Veterinário (staff)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return self.username

class Perfil(models.Model):
    """
    Modelo abstrato base para perfis de usuário.
    
    Contém dados pessoais compartilhados entre Dono e Funcionário.
    
    Campos:
    - usuario: Relação one-to-one com Usuario
    - nome: Nome completo
    - cpf: CPF único
    - endereco: Endereço completo
    - telefone: Telefone de contato
    - created_at: Data de criação
    - updated_at: Data de última atualização
    """
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
    """
    Modelo para perfil de dono de pets.
    
    Representa um proprietário que pode registrar pets na clínica.
    Herda todos os campos do Perfil base.
    """
    class Meta:
        db_table = 'perfil_dono'

class PerfilFuncionario(Perfil):
    """
    Modelo para perfil de funcionário/veterinário.
    
    Representa um membro da equipe que pode registrar vacinações.
    
    Campos adicionais:
    - cargo: Função/cargo do funcionário (ex: Veterinário, Técnico)
    """
    cargo = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'perfil_funcionario'

    def __str__(self):
        return f"{self.nome} - {self.cargo}"