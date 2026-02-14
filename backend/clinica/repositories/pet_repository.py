"""
Repositório de Pets.

Responsável pelo acesso a dados de pets, seguindo o padrão Repository.
"""

from typing import List, Optional
from django.db.models import QuerySet
from ..models import Pet
from usuarios.models import PerfilDono


class PetRepository:
    """Repositório para operações de acesso a dados de Pets."""
    
    @staticmethod
    def get_all() -> QuerySet:
        """Retorna todos os pets."""
        return Pet.objects.all()
    
    @staticmethod
    def get_by_id(pet_id: int) -> Optional[Pet]:
        """
        Retorna um pet pelo ID.
        
        Args:
            pet_id: ID do pet
            
        Returns:
            Pet ou None se não encontrado
        """
        try:
            return Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_owner(dono: PerfilDono) -> QuerySet:
        """
        Retorna todos os pets de um dono específico.
        
        Args:
            dono: Instância de PerfilDono
            
        Returns:
            QuerySet de pets do dono
        """
        return Pet.objects.filter(dono=dono)
    
    @staticmethod
    def create(
        dono: PerfilDono,
        nome: str,
        especie: str,
        raca: str,
        peso: float,
        data_nascimento: Optional[str] = None
    ) -> Pet:
        """
        Cria um novo pet.
        
        Args:
            dono: PerfilDono proprietário
            nome: Nome do pet
            especie: Espécie (Cachorro, Gato, etc)
            raca: Raça
            peso: Peso em kg
            data_nascimento: Data de nascimento (opcional)
            
        Returns:
            Pet criado
        """
        return Pet.objects.create(
            dono=dono,
            nome=nome,
            especie=especie,
            raca=raca,
            peso=peso,
            data_nascimento=data_nascimento
        )
    
    @staticmethod
    def update(
        pet: Pet,
        nome: Optional[str] = None,
        especie: Optional[str] = None,
        raca: Optional[str] = None,
        peso: Optional[float] = None,
        data_nascimento: Optional[str] = None
    ) -> Pet:
        """
        Atualiza um pet.
        
        Args:
            pet: Instância de Pet a atualizar
            **kwargs: Campos a atualizar
            
        Returns:
            Pet atualizado
        """
        if nome is not None:
            pet.nome = nome
        if especie is not None:
            pet.especie = especie
        if raca is not None:
            pet.raca = raca
        if peso is not None:
            pet.peso = peso
        if data_nascimento is not None:
            pet.data_nascimento = data_nascimento
        
        pet.save()
        return pet
    
    @staticmethod
    def delete(pet: Pet) -> None:
        """
        Deleta um pet.
        
        Args:
            pet: Instância de Pet a deletar
        """
        pet.delete()
    
    @staticmethod
    def exists(pet_id: int) -> bool:
        """
        Verifica se um pet existe.
        
        Args:
            pet_id: ID do pet
            
        Returns:
            True se existe, False caso contrário
        """
        return Pet.objects.filter(id=pet_id).exists()
