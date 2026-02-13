from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date
from decimal import Decimal
from usuarios.models import PerfilDono, PerfilFuncionario

class Pet(models.Model):
    dono = models.ForeignKey(
        PerfilDono, 
        on_delete=models.PROTECT, 
        related_name='pets'
    )
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=100)
    raca = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    data_nascimento = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet'

    def __str__(self):
        return f"{self.nome} ({self.dono.nome})"
    
    def calcular_idade_dias(self):
        if not self.data_nascimento:
            return None
        return (timezone.now().date() - self.data_nascimento).days
    
    def calcular_idade_anos(self):
        dias = self.calcular_idade_dias()
        if dias is None:
            return None
        return dias // 365
    
    def listar_proximas_doses(self):
        hoje = date.today()
        proximas = []

        for historico in self.historico_vacinas.all().order_by('-data_aplicacao'): # type: ignore
            if historico.proxima_dose and historico.proxima_dose >= hoje:
                proximas.append({
                    'vacina': historico.vacina.nome,
                    'data_proxima_dose': historico.proxima_dose,
                    'dias_restantes': (historico.proxima_dose - hoje).days,
                    'historico_id': historico.id
                })
        return proximas
    
    def listar_doses_vencidas(self):
        hoje = date.today()
        vencidas = []

        for historico in self.historico_vacinas.all().order_by('-data_aplicacao'): # type: ignore
            if historico.proxima_dose and historico.proxima_dose < hoje:
                dias = (hoje - historico.proxima_dose).days
                vencidas.append({
                    'vacina': historico.vacina.nome,
                    'data_proxima_dose': historico.proxima_dose,
                    'dias_vencido': dias,
                    'historico_id': historico.id
                })
        return vencidas

class Vacina(models.Model):
    nome = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))]) 
    intervalo_doses_dias = models.PositiveIntegerField()
    descricao = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vacina'

    def __str__(self):
        return self.nome

class PetVacina(models.Model):
    pet = models.ForeignKey(
        Pet, 
        on_delete=models.PROTECT, 
        related_name='historico_vacinas'
    )
    vacina = models.ForeignKey(
        Vacina, 
        on_delete=models.PROTECT, 
        related_name='aplicacoes'
    )
    aplicador = models.ForeignKey(
        PerfilFuncionario, 
        on_delete=models.PROTECT, 
        related_name='vacinas_aplicadas'
    )
    data_aplicacao = models.DateField()
    proxima_dose = models.DateField(null=True, blank=True)
    lote = models.CharField(max_length=50)
    observacoes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pet_vacina'

    def __str__(self):
        return f"{self.vacina.nome} -> {self.pet.nome}"