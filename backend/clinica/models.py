from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from usuarios.models import PerfilDono, PerfilFuncionario

class Pet(models.Model):
    """
    Modelo para registrar pets na clínica.
    
    Campos:
    - dono: FK para PerfilDono (quem é dono)
    - nome: Nome do pet
    - especie: Ex: Cachorro, Gato
    - raca: Raça/tipo do pet
    - peso: Peso em kg (mínimo 0.01)
    - data_nascimento: Data de nascimento (opcional)
    - created_at: Data de registro
    - updated_at: Data de última atualização
    
    Métodos:
    - calcular_idade_dias(): Retorna idade em dias
    - calcular_idade_anos(): Retorna idade em anos
    - obter_proximas_doses(): Lista de próximas vacinas
    - obter_doses_vencidas(): Lista de vacinas atrasadas
    """
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
        """Calcula idade em dias baseado na data de nascimento"""
        if not self.data_nascimento:
            return None
        return (timezone.now().date() - self.data_nascimento).days
    
    def calcular_idade_anos(self):
        """Calcula idade em anos (divisão inteira de dias por 365)"""
        dias = self.calcular_idade_dias()
        if dias is None:
            return None
        return dias // 365
    
    def obter_proximas_doses(self):
        """Retorna lista de próximas doses ainda não vencidas"""
        hoje = date.today()
        proximas = []
        
        for registro in self.historico_vacinas.all().order_by('-data_aplicacao'): # type: ignore
            if registro.proxima_dose and registro.proxima_dose >= hoje:
                proximas.append({
                    'vacina': registro.vacina.nome,
                    'data_proxima_dose': registro.proxima_dose,
                    'dias_restantes': (registro.proxima_dose - hoje).days,
                    'historico_id': registro.id
                })
        return proximas
    
    def obter_doses_vencidas(self):
        """Retorna lista de doses em atraso"""
        hoje = date.today()
        vencidas = []
        
        for registro in self.historico_vacinas.all().order_by('-data_aplicacao'): # type: ignore
            if registro.proxima_dose and registro.proxima_dose < hoje:
                dias = (hoje - registro.proxima_dose).days
                vencidas.append({
                    'vacina': registro.vacina.nome,
                    'data_proxima_dose': registro.proxima_dose,
                    'dias_vencido': dias,
                    'historico_id': registro.id
                })
        return vencidas

class Vacina(models.Model):
    """
    Modelo para catálogo de vacinas disponíveis na clínica.
    
    Campos:
    - nome: Nome da vacina (ex: Raiva, Polivalente)
    - fabricante: Laboratório/fabricante
    - valor: Preço em R$
    - intervalo_doses_dias: Dias entre aplicações (ex: 365 para anual)
    - descricao: Descrição detalhada da vacina
    - created_at: Data de registro
    - updated_at: Data de última atualização
    
    Relacionamentos:
    - aplicacoes: Relacionamento reverso com PetVacina (múltiplas aplicações)
    """
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
    """
    Modelo para registrar aplicações de vacinas em pets.
    
    Campos:
    - pet: FK para Pet (qual pet foi vacinado)
    - vacina: FK para Vacina (qual vacina foi aplicada)
    - aplicador: FK para PerfilFuncionario (quem aplicou)
    - data_aplicacao: Data que foi aplicada
    - proxima_dose: Data da próxima dose (calculada automaticamente)
    - lote: Lote/número do frasco
    - observacoes: Anotações adicionais
    - created_at: Data de registro
    - updated_at: Data de última atualização
    
    Regra de Negócio:
    - Próxima dose é calculada automaticamente = data_aplicacao + vacina.intervalo_doses_dias
    - Status é definido automaticamente baseado nos dias para próxima dose
    
    Métodos:
    - esta_vencida(): Verifica se passou da próxima dose
    - get_status(): Retorna status (em_dia, proxima_em_breve, vencida, indefinido)
    """
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
    
    def save(self, *args, **kwargs):
        """Calcula próxima dose automaticamente ao salvar"""
        if not self.proxima_dose:
            self.proxima_dose = self.data_aplicacao + timedelta(
                days=self.vacina.intervalo_doses_dias
            )
        super().save(*args, **kwargs)

    def esta_vencida(self):
        """Verifica se a próxima dose já passou de hoje"""
        if not self.proxima_dose:
            return False
        return self.proxima_dose < date.today()

    def get_status(self):
        """
        Retorna o status automático da vacinação.
        
        Retorna:
        - 'em_dia': Próxima dose > 7 dias
        - 'proxima_em_breve': Próxima dose em até 7 dias
        - 'vencida': Próxima dose passou
        - 'indefinido': Sem próxima dose definida
        """
        hoje = date.today()
        
        if not self.proxima_dose:
            return "indefinido"
        
        if self.proxima_dose < hoje:
            return "vencida"
        elif (self.proxima_dose - hoje).days <= 7:
            return "proxima_em_breve"
        else:
            return "em_dia"