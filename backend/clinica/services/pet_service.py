"""
Serviço de Pets.

Contém a lógica de negócio para operações com Pets.
Segue o padrão Service, separando do acesso a dados (Repository).
"""

from typing import List, Optional, Dict, Any
from logging import Logger
from datetime import date

from core.exceptions import (
    PetNotFoundException,
    StaffOnlyException,
    OwnerAccessOnlyException,
)
from core.constants import VALIDATION_CONSTRAINTS, ERROR_MESSAGES
from core.logging_config import DomainLoggers
from usuarios.models import Usuario, PerfilDono
from ..models import Pet
from .repositories_builder import get_pet_repository

logger = DomainLoggers.get_pet_logger()


class PetService:
    """Serviço para gerenciar operações com Pets."""
    
    def __init__(self):
        self.repository = get_pet_repository()
    
    def list_all_pets(self, user: Usuario) -> List[Pet]:
        """
        Lista todos os pets conforme permissões do usuário.
        
        - Staff vê todos os pets
        - Donos veem apenas seus pets
        
        Args:
            user: Usuário autenticado
            
        Returns:
            Lista de pets
            
        Raises:
            OwnerAccessOnlyException: Se dono não possui perfil
        """
        logger.info(f"Listando pets para usuário: {user.username}")
        
        if user.is_staff:
            logger.info(f"Usuário {user.username} é staff, retornando todos os pets")
            return list(self.repository.get_all())
        
        try:
            dono = PerfilDono.objects.get(usuario=user)
            pets = list(self.repository.get_by_owner(dono))
            logger.info(f"Retornados {len(pets)} pets para dono {dono.nome}")
            return pets
        except PerfilDono.DoesNotExist:
            logger.error(f"Dono não encontrado para usuário {user.username}")
            raise OwnerAccessOnlyException(ERROR_MESSAGES.OWNER_PROFILE_NOT_FOUND)
    
    def get_pet_by_id(self, pet_id: int) -> Pet:
        """
        Obtém um pet pelo ID.
        
        Args:
            pet_id: ID do pet
            
        Returns:
            Instância de Pet
            
        Raises:
            PetNotFoundException: Se pet não existe
        """
        pet = self.repository.get_by_id(pet_id)
        
        if not pet:
            logger.warning(f"Pet com ID {pet_id} não encontrado")
            raise PetNotFoundException(
                message=f"Pet com ID {pet_id} não encontrado"
            )
        
        logger.info(f"Pet {pet.nome} (ID: {pet_id}) recuperado")
        return pet
    
    def create_pet(
        self,
        user: Usuario,
        dono_id: Optional[int],
        nome: str,
        especie: str,
        raca: str,
        peso: float,
        data_nascimento: Optional[date] = None
    ) -> Pet:
        """
        Cria um novo pet com validações de permissão.
        
        - Donos: Só podem criar para si mesmos
        - Staff: Pode criar para qualquer dono
        
        Args:
            user: Usuário autenticado
            dono_id: ID do dono (se staff)
            nome: Nome do pet
            especie: Espécie
            raca: Raça
            peso: Peso em kg
            data_nascimento: Data de nascimento
            
        Returns:
            Pet criado
            
        Raises:
            OwnerAccessOnlyException: Se usuário tenta criar para outro
            ValueError: Se dados são inválidos
        """
        logger.info(f"Criando novo pet: {nome} (usuário: {user.username})")
        
        if peso < VALIDATION_CONSTRAINTS.MIN_PET_WEIGHT:
            logger.error(f"Peso inválido para pet {nome}: {peso}")
            raise ValueError(f"Peso mínimo é {VALIDATION_CONSTRAINTS.MIN_PET_WEIGHT}kg")
        
        if dono_id:
            if not user.is_staff:
                dono = self._get_user_owner(user)
                if dono.id != dono_id:
                    logger.warning(
                        f"Usuário {user.username} tentou criar pet para dono {dono_id}"
                    )
                    raise OwnerAccessOnlyException(ERROR_MESSAGES.OWN_PETS_ONLY)
            else:
                dono = PerfilDono.objects.get(id=dono_id)
        else:
            dono = self._get_user_owner(user)
        
        pet = self.repository.create(
            dono=dono,
            nome=nome,
            especie=especie,
            raca=raca,
            peso=peso,
            data_nascimento=data_nascimento
        )
        
        logger.info(f"Pet criado com sucesso: {pet.nome} (ID: {pet.id}, Dono: {dono.nome})")
        return pet
    
    def update_pet(
        self,
        user: Usuario,
        pet_id: int,
        **kwargs
    ) -> Pet:
        """
        Atualiza um pet com validações de permissão.
        
        Args:
            user: Usuário autenticado
            pet_id: ID do pet
            **kwargs: Campos a atualizar
            
        Returns:
            Pet atualizado
            
        Raises:
            PetNotFoundException: Se pet não existe
            OwnerAccessOnlyException: Se usuário não tem permissão
        """
        pet = self.get_pet_by_id(pet_id)
        
        if not user.is_staff:
            dono = self._get_user_owner(user)
            if pet.dono != dono:
                logger.warning(
                    f"Usuário {user.username} tentou atualizar pet de outro dono"
                )
                raise OwnerAccessOnlyException(ERROR_MESSAGES.OWN_PETS_EDIT)
        
        if 'peso' in kwargs and kwargs['peso'] < VALIDATION_CONSTRAINTS.MIN_PET_WEIGHT:
            logger.error(f"Peso inválido ao atualizar pet {pet_id}")
            raise ValueError(f"Peso mínimo é {VALIDATION_CONSTRAINTS.MIN_PET_WEIGHT}kg")
        
        pet = self.repository.update(pet, **kwargs)
        logger.info(f"Pet {pet.nome} (ID: {pet_id}) atualizado")
        return pet
    
    def delete_pet(self, user: Usuario, pet_id: int) -> None:
        """
        Deleta um pet com validações de permissão.
        
        Args:
            user: Usuário autenticado
            pet_id: ID do pet
            
        Raises:
            PetNotFoundException: Se pet não existe
            OwnerAccessOnlyException: Se usuário não tem permissão
        """
        pet = self.get_pet_by_id(pet_id)
        
        if not user.is_staff:
            dono = self._get_user_owner(user)
            if pet.dono != dono:
                logger.warning(
                    f"Usuário {user.username} tentou deletar pet de outro dono"
                )
                raise OwnerAccessOnlyException(ERROR_MESSAGES.OWN_PETS_DELETE)
        
        logger.info(f"Deletando pet {pet.nome} (ID: {pet_id})")
        self.repository.delete(pet)
        logger.info(f"Pet {pet.nome} deletado com sucesso")
    
    def get_pet_vaccination_history(self, pet_id: int) -> List[Dict[str, Any]]:
        """
        Obtém histórico de vacinação de um pet.
        
        Args:
            pet_id: ID do pet
            
        Returns:
            Lista com histórico de vacinações
            
        Raises:
            PetNotFoundException: Se pet não existe
        """
        pet = self.get_pet_by_id(pet_id)
        logger.info(f"Recuperando histórico de vacinação para pet {pet.nome}")
        return pet.obter_proximas_doses() + pet.obter_doses_vencidas()
    
    def _get_user_owner(self, user: Usuario) -> PerfilDono:
        """
        Obtém o PerfilDono associado ao usuário.
        
        Args:
            user: Usuário autenticado
            
        Returns:
            PerfilDono do usuário
            
        Raises:
            OwnerAccessOnlyException: Se usuário não é dono
        """
        try:
            return PerfilDono.objects.get(usuario=user)
        except PerfilDono.DoesNotExist:
            logger.error(f"PerfilDono não encontrado para usuário {user.username}")
            raise OwnerAccessOnlyException(ERROR_MESSAGES.OWNER_PROFILE_NOT_FOUND)
