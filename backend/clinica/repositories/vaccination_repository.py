"""
Repositório de Histórico de Vacinação.

Responsável pelo acesso a dados de registros de vacinação aplicadas.
"""

from typing import Optional, List
from datetime import datetime, date
from django.db.models import QuerySet
from ..models import PetVacina, Pet
from usuarios.models import PerfilDono, PerfilFuncionario


class PetVaccineRepository:
    """Repositório para operações de acesso a dados de PetVacina."""
    
    @staticmethod
    def get_all() -> QuerySet:
        """Retorna todos os registros de vacinação."""
        return PetVacina.objects.all()
    
    @staticmethod
    def get_by_id(record_id: int) -> Optional[PetVacina]:
        """
        Retorna um registro de vacinação pelo ID.
        
        Args:
            record_id: ID do registro
            
        Returns:
            PetVacina ou None se não encontrado
        """
        try:
            return PetVacina.objects.get(id=record_id)
        except PetVacina.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_pet(pet: Pet) -> QuerySet:
        """
        Retorna todo histórico de vacinação de um pet.
        
        Args:
            pet: Instância de Pet
            
        Returns:
            QuerySet de registros de vacinação
        """
        return PetVacina.objects.filter(pet=pet).order_by('-data_aplicacao')
    
    @staticmethod
    def get_by_owner(dono: PerfilDono) -> QuerySet:
        """
        Retorna registros de vacinação de todos os pets de um dono.
        
        Args:
            dono: Instância de PerfilDono
            
        Returns:
            QuerySet de registros de vacinação
        """
        return PetVacina.objects.filter(pet__dono=dono)
    
    @staticmethod
    def get_overdue_vaccinations() -> QuerySet:
        """
        Retorna todos os registros de vacinação vencidos.
        
        Returns:
            QuerySet de registros vencidos
        """
        today = date.today()
        return PetVacina.objects.filter(
            proxima_dose__lt=today,
            proxima_dose__isnull=False
        ).order_by('proxima_dose')
    
    @staticmethod
    def get_upcoming_vaccinations(days_threshold: int = 7) -> QuerySet:
        """
        Retorna registros de vacinação próximos de vencer.
        
        Args:
            days_threshold: Número de dias para considerar "próximo"
            
        Returns:
            QuerySet de registros próximos de vencer
        """
        today = date.today()
        from datetime import timedelta
        threshold_date = today + timedelta(days=days_threshold)
        
        return PetVacina.objects.filter(
            proxima_dose__gte=today,
            proxima_dose__lte=threshold_date,
            proxima_dose__isnull=False
        ).order_by('proxima_dose')
    
    @staticmethod
    def create(
        pet: Pet,
        vacina,
        aplicador: PerfilFuncionario,
        data_aplicacao: date,
        lote: str,
        observacoes: str = ""
    ) -> PetVacina:
        """
        Cria um novo registro de vacinação.
        
        Args:
            pet: Pet que foi vacinado
            vacina: Vacina aplicada
            aplicador: Funcionário que aplicou
            data_aplicacao: Data da aplicação
            lote: Lote da vacina
            observacoes: Observações adicionais
            
        Returns:
            PetVacina criado
        """
        return PetVacina.objects.create(
            pet=pet,
            vacina=vacina,
            aplicador=aplicador,
            data_aplicacao=data_aplicacao,
            lote=lote,
            observacoes=observacoes
        )
    
    @staticmethod
    def update(
        vaccination: PetVacina,
        lote: Optional[str] = None,
        observacoes: Optional[str] = None,
        proxima_dose: Optional[date] = None
    ) -> PetVacina:
        """
        Atualiza um registro de vacinação.
        
        Args:
            vaccination: Instância de PetVacina a atualizar
            lote: Novo lote (opcional)
            observacoes: Novas observações (opcional)
            proxima_dose: Nova data de próxima dose (opcional)
            
        Returns:
            PetVacina atualizado
        """
        if lote is not None:
            vaccination.lote = lote
        if observacoes is not None:
            vaccination.observacoes = observacoes
        if proxima_dose is not None:
            vaccination.proxima_dose = proxima_dose
        
        vaccination.save()
        return vaccination
    
    @staticmethod
    def delete(vaccination: PetVacina) -> None:
        """
        Deleta um registro de vacinação.
        
        Args:
            vaccination: Instância de PetVacina a deletar
        """
        vaccination.delete()
    
    @staticmethod
    def exists(record_id: int) -> bool:
        """
        Verifica se um registro de vacinação existe.
        
        Args:
            record_id: ID do registro
            
        Returns:
            True se existe, False caso contrário
        """
        return PetVacina.objects.filter(id=record_id).exists()
