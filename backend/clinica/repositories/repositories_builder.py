"""
Factory para criação de repositórios.

Centraliza a instanciação de repositórios, facilitando
testes e injeção de dependência.
"""

from .pet_repository import PetRepository
from .vaccine_repository import VaccineRepository
from .vaccination_repository import PetVaccineRepository


def get_pet_repository() -> PetRepository:
    """Retorna instância de PetRepository."""
    return PetRepository()


def get_vaccine_repository() -> VaccineRepository:
    """Retorna instância de VaccineRepository."""
    return VaccineRepository()


def get_vaccination_repository() -> PetVaccineRepository:
    """Retorna instância de PetVaccineRepository."""
    return PetVaccineRepository()
