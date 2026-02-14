"""
Serviço de Vacinação.

Contém a lógica de negócio para operações com Vacinação.
"""

from typing import List, Optional
from logging import Logger
from datetime import date, timedelta

from core.exceptions import (
    VaccineNotFoundException,
    StaffOnlyException,
    VaccinationLogicException,
)
from core.constants import (
    VACCINATION_CONSTANTS,
    VACCINATION_STATUS,
    ERROR_MESSAGES,
)
from core.logging_config import DomainLoggers
from usuarios.models import Usuario, PerfilFuncionario
from ..models import Vacina, PetVacina, Pet
from .repositories_builder import (
    get_vaccine_repository,
    get_vaccination_repository,
    get_pet_repository,
)

logger = DomainLoggers.get_vacina_logger()


class VaccineService:
    """Serviço para gerenciar operações com Vacinas."""
    
    def __init__(self):
        self.repository = get_vaccine_repository()
    
    def list_all_vaccines(self) -> List[Vacina]:
        """
        Lista todas as vacinas disponíveis.
        
        Returns:
            Lista de vacinas
        """
        logger.info("Listando todas as vacinas")
        vaccines = list(self.repository.get_all())
        logger.info(f"Total de {len(vaccines)} vacinas encontradas")
        return vaccines
    
    def get_vaccine_by_id(self, vaccine_id: int) -> Vacina:
        """
        Obtém uma vacina pelo ID.
        
        Args:
            vaccine_id: ID da vacina
            
        Returns:
            Instância de Vacina
            
        Raises:
            VaccineNotFoundException: Se vacina não existe
        """
        vaccine = self.repository.get_by_id(vaccine_id)
        
        if not vaccine:
            logger.warning(f"Vacina com ID {vaccine_id} não encontrada")
            raise VaccineNotFoundException(
                message=f"Vacina com ID {vaccine_id} não encontrada"
            )
        
        logger.info(f"Vacina {vaccine.nome} (ID: {vaccine_id}) recuperada")
        return vaccine
    
    def create_vaccine(
        self,
        user: Usuario,
        nome: str,
        fabricante: str,
        valor: float,
        intervalo_doses_dias: int,
        descricao: str
    ) -> Vacina:
        """
        Cria uma nova vacina (apenas staff).
        
        Args:
            user: Usuário autenticado
            nome: Nome da vacina
            fabricante: Fabricante
            valor: Valor em R$
            intervalo_doses_dias: Dias entre doses
            descricao: Descrição
            
        Returns:
            Vacina criada
            
        Raises:
            StaffOnlyException: Se usuário não é staff
            ValueError: Se dados são inválidos
        """
        self._validate_staff(user)
        
        logger.info(f"Staff {user.username} criando nova vacina: {nome}")
        
        # Validações
        if valor < 0:
            logger.error(f"Valor negativo para vacina {nome}")
            raise ValueError("Valor não pode ser negativo")
        
        if intervalo_doses_dias <= 0:
            logger.error(f"Intervalo inválido para vacina {nome}")
            raise ValueError("Intervalo de doses deve ser maior que zero")
        
        vaccine = self.repository.create(
            nome=nome,
            fabricante=fabricante,
            valor=valor,
            intervalo_doses_dias=intervalo_doses_dias,
            descricao=descricao
        )
        
        logger.info(f"Vacina criada com sucesso: {vaccine.nome} (ID: {vaccine.id})")
        return vaccine
    
    def update_vaccine(
        self,
        user: Usuario,
        vaccine_id: int,
        **kwargs
    ) -> Vacina:
        """
        Atualiza uma vacina (apenas staff).
        
        Args:
            user: Usuário autenticado
            vaccine_id: ID da vacina
            **kwargs: Campos a atualizar
            
        Returns:
            Vacina atualizada
            
        Raises:
            StaffOnlyException: Se usuário não é staff
            VaccineNotFoundException: Se vacina não existe
        """
        self._validate_staff(user)
        vaccine = self.get_vaccine_by_id(vaccine_id)
        
        logger.info(f"Staff {user.username} atualizando vacina {vaccine.nome}")
        
        # Validações
        if 'valor' in kwargs and kwargs['valor'] < 0:
            logger.error(f"Valor negativo para vacina {vaccine_id}")
            raise ValueError("Valor não pode ser negativo")
        
        if 'intervalo_doses_dias' in kwargs:
            if kwargs['intervalo_doses_dias'] <= 0:
                logger.error(f"Intervalo inválido para vacina {vaccine_id}")
                raise ValueError("Intervalo deve ser maior que zero")
        
        vaccine = self.repository.update(vaccine, **kwargs)
        logger.info(f"Vacina {vaccine.nome} atualizada com sucesso")
        return vaccine
    
    def delete_vaccine(self, user: Usuario, vaccine_id: int) -> None:
        """
        Deleta uma vacina (apenas staff).
        
        Args:
            user: Usuário autenticado
            vaccine_id: ID da vacina
            
        Raises:
            StaffOnlyException: Se usuário não é staff
            VaccineNotFoundException: Se vacina não existe
        """
        self._validate_staff(user)
        vaccine = self.get_vaccine_by_id(vaccine_id)
        
        logger.info(f"Staff {user.username} deletando vacina {vaccine.nome}")
        self.repository.delete(vaccine)
        logger.info(f"Vacina {vaccine.nome} deletada com sucesso")
    
    def _validate_staff(self, user: Usuario) -> None:
        """
        Valida se usuário é staff.
        
        Args:
            user: Usuário a validar
            
        Raises:
            StaffOnlyException: Se não é staff
        """
        if not user.is_staff:
            logger.warning(f"Usuário não-staff {user.username} tentou operação restrita")
            raise StaffOnlyException(ERROR_MESSAGES.STAFF_ONLY)


class VaccinationService:
    """Serviço para gerenciar registros de vacinação."""
    
    def __init__(self):
        self.vaccination_repo = get_vaccination_repository()
        self.pet_repo = get_pet_repository()
        self.vaccine_repo = get_vaccine_repository()
    
    def list_all_vaccinations(self, user: Usuario) -> List[PetVacina]:
        """
        Lista registros de vacinação conforme permissões.
        
        - Staff vê todos
        - Donos veem apenas seus pets
        
        Args:
            user: Usuário autenticado
            
        Returns:
            Lista de registros de vacinação
        """
        logger.info(f"Listando vacinações para usuário {user.username}")
        
        if user.is_staff:
            return list(self.vaccination_repo.get_all())
        
        try:
            dono = PerfilFuncionario.objects.get(usuario=user)
            return list(self.vaccination_repo.get_by_owner(dono))
        except PerfilFuncionario.DoesNotExist:
            logger.warning(f"Dono não encontrado para usuário {user.username}")
            return []
    
    def get_vaccination_by_id(self, vaccination_id: int) -> PetVacina:
        """
        Obtém um registro de vacinação pelo ID.
        
        Args:
            vaccination_id: ID do registro
            
        Returns:
            Registro de vacinação
            
        Raises:
            VaccinationLogicException: Se não existe
        """
        vaccination = self.vaccination_repo.get_by_id(vaccination_id)
        
        if not vaccination:
            logger.warning(f"Registro de vacinação {vaccination_id} não encontrado")
            raise VaccinationLogicException(
                message=f"Registro de vacinação {vaccination_id} não encontrado"
            )
        
        return vaccination
    
    def record_vaccination(
        self,
        user: Usuario,
        pet_id: int,
        vaccine_id: int,
        aplicador_id: int,
        data_aplicacao: date,
        lote: str,
        observacoes: str = ""
    ) -> PetVacina:
        """
        Registra uma nova aplicação de vacina (apenas staff).
        
        Args:
            user: Usuário autenticado
            pet_id: ID do pet vacinado
            vaccine_id: ID da vacina aplicada
            aplicador_id: ID do funcionário que aplicou
            data_aplicacao: Data da aplicação
            lote: Lote da vacina
            observacoes: Observações adicionais
            
        Returns:
            Registro de vacinação criado
            
        Raises:
            StaffOnlyException: Se usuário não é staff
            ValueError: Se dados são inválidos
        """
        self._validate_staff(user)
        
        logger.info(
            f"Staff {user.username} registrando vacinação:"
            f" pet={pet_id}, vaccine={vaccine_id}"
        )
        
        # Validar referências
        pet = self.pet_repo.get_by_id(pet_id)
        if not pet:
            logger.error(f"Pet {pet_id} não encontrado")
            raise ValueError(f"Pet {pet_id} não encontrado")
        
        vaccine = self.vaccine_repo.get_by_id(vaccine_id)
        if not vaccine:
            logger.error(f"Vacina {vaccine_id} não encontrada")
            raise ValueError(f"Vacina {vaccine_id} não encontrada")
        
        try:
            aplicador = PerfilFuncionario.objects.get(id=aplicador_id)
        except PerfilFuncionario.DoesNotExist:
            logger.error(f"Funcionário {aplicador_id} não encontrado")
            raise ValueError(f"Funcionário {aplicador_id} não encontrado")
        
        # Validar data
        if data_aplicacao > date.today():
            logger.error(f"Data de aplicação futura: {data_aplicacao}")
            raise ValueError("Data de aplicação não pode ser no futuro")
        
        # Criar registro
        vaccination = self.vaccination_repo.create(
            pet=pet,
            vacina=vaccine,
            aplicador=aplicador,
            data_aplicacao=data_aplicacao,
            lote=lote,
            observacoes=observacoes
        )
        
        logger.info(
            f"Vacinação registrada com sucesso:"
            f" {vaccine.nome} em {pet.nome} (ID: {vaccination.id})"
        )
        return vaccination
    
    def update_vaccination(
        self,
        user: Usuario,
        vaccination_id: int,
        **kwargs
    ) -> PetVacina:
        """
        Atualiza um registro de vacinação (apenas staff).
        
        Args:
            user: Usuário autenticado
            vaccination_id: ID do registro
            **kwargs: Campos a atualizar
            
        Returns:
            Registro atualizado
            
        Raises:
            StaffOnlyException: Se usuário não é staff
        """
        self._validate_staff(user)
        vaccination = self.get_vaccination_by_id(vaccination_id)
        
        logger.info(f"Staff {user.username} atualizando vacinação {vaccination_id}")
        
        vaccination = self.vaccination_repo.update(vaccination, **kwargs)
        logger.info(f"Vacinação {vaccination_id} atualizada com sucesso")
        return vaccination
    
    def delete_vaccination(self, user: Usuario, vaccination_id: int) -> None:
        """
        Deleta um registro de vacinação (apenas staff).
        
        Args:
            user: Usuário autenticado
            vaccination_id: ID do registro
            
        Raises:
            StaffOnlyException: Se usuário não é staff
        """
        self._validate_staff(user)
        vaccination = self.get_vaccination_by_id(vaccination_id)
        
        logger.info(f"Staff {user.username} deletando vacinação {vaccination_id}")
        self.vaccination_repo.delete(vaccination)
        logger.info(f"Vacinação {vaccination_id} deletada com sucesso")
    
    def get_vaccination_status(self, vaccination: PetVacina) -> str:
        """
        Calcula o status automático de uma vacinação.
        
        Args:
            vaccination: Registro de vacinação
            
        Returns:
            Status: 'em_dia', 'proxima_em_breve', 'vencida' ou 'indefinido'
        """
        return vaccination.get_status()
    
    def get_upcoming_vaccinations(self, days_threshold: int = 7) -> List[PetVacina]:
        """
        Lista próximas vacinações próximas de vencer.
        
        Args:
            days_threshold: Número de dias de limiar
            
        Returns:
            Lista de vacinações próximas
        """
        logger.info(f"Listando vacinações próximas (limiar: {days_threshold} dias)")
        return list(self.vaccination_repo.get_upcoming_vaccinations(days_threshold))
    
    def get_overdue_vaccinations(self) -> List[PetVacina]:
        """
        Lista vacinações vencidas.
        
        Returns:
            Lista de vacinações vencidas
        """
        logger.info("Listando vacinações vencidas")
        return list(self.vaccination_repo.get_overdue_vaccinations())
    
    def _validate_staff(self, user: Usuario) -> None:
        """
        Valida se usuário é staff.
        
        Args:
            user: Usuário a validar
            
        Raises:
            StaffOnlyException: Se não é staff
        """
        if not user.is_staff:
            logger.warning(f"Usuário não-staff {user.username} tentou operação de vacinação")
            raise StaffOnlyException(ERROR_MESSAGES.STAFF_ONLY)
