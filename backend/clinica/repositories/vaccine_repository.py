"""
Repositório de Vacinas.

Responsável pelo acesso a dados de vacinas.
"""

from typing import List, Optional
from django.db.models import QuerySet
from ..models import Vacina


class VaccineRepository:
    """Repositório para operações de acesso a dados de Vacinas."""
    
    @staticmethod
    def get_all() -> QuerySet:
        """Retorna todas as vacinas."""
        return Vacina.objects.all()
    
    @staticmethod
    def get_by_id(vaccine_id: int) -> Optional[Vacina]:
        """
        Retorna uma vacina pelo ID.
        
        Args:
            vaccine_id: ID da vacina
            
        Returns:
            Vacina ou None se não encontrada
        """
        try:
            return Vacina.objects.get(id=vaccine_id)
        except Vacina.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_name(name: str) -> Optional[Vacina]:
        """
        Retorna uma vacina pelo nome.
        
        Args:
            name: Nome da vacina
            
        Returns:
            Vacina ou None se não encontrada
        """
        try:
            return Vacina.objects.get(nome=name)
        except Vacina.DoesNotExist:
            return None
    
    @staticmethod
    def create(
        nome: str,
        fabricante: str,
        valor: float,
        intervalo_doses_dias: int,
        descricao: str
    ) -> Vacina:
        """
        Cria uma nova vacina.
        
        Args:
            nome: Nome da vacina
            fabricante: Laboratório/fabricante
            valor: Preço em R$
            intervalo_doses_dias: Dias entre doses
            descricao: Descrição
            
        Returns:
            Vacina criada
        """
        return Vacina.objects.create(
            nome=nome,
            fabricante=fabricante,
            valor=valor,
            intervalo_doses_dias=intervalo_doses_dias,
            descricao=descricao
        )
    
    @staticmethod
    def update(
        vaccine: Vacina,
        nome: Optional[str] = None,
        fabricante: Optional[str] = None,
        valor: Optional[float] = None,
        intervalo_doses_dias: Optional[int] = None,
        descricao: Optional[str] = None
    ) -> Vacina:
        """
        Atualiza uma vacina.
        
        Args:
            vaccine: Instância de Vacina a atualizar
            **kwargs: Campos a atualizar
            
        Returns:
            Vacina atualizada
        """
        if nome is not None:
            vaccine.nome = nome
        if fabricante is not None:
            vaccine.fabricante = fabricante
        if valor is not None:
            vaccine.valor = valor
        if intervalo_doses_dias is not None:
            vaccine.intervalo_doses_dias = intervalo_doses_dias
        if descricao is not None:
            vaccine.descricao = descricao
        
        vaccine.save()
        return vaccine
    
    @staticmethod
    def delete(vaccine: Vacina) -> None:
        """
        Deleta uma vacina.
        
        Args:
            vaccine: Instância de Vacina a deletar
        """
        vaccine.delete()
    
    @staticmethod
    def exists(vaccine_id: int) -> bool:
        """
        Verifica se uma vacina existe.
        
        Args:
            vaccine_id: ID da vacina
            
        Returns:
            True se existe, False caso contrário
        """
        return Vacina.objects.filter(id=vaccine_id).exists()
