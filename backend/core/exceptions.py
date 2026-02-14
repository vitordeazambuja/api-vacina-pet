"""
Exceções customizadas da aplicação.

Define exceções específicas do domínio para melhor tratamento de erros
e separação de responsabilidades.
"""

from typing import Dict, Any, Optional


class APIException(Exception):
    """
    Exceção base para todas as exceções da API.
    
    Atributos:
        message: Mensagem de erro amigável ao usuário
        status_code: Código HTTP apropriado
        detail: Detalhes técnicos adicionais
    """
    
    status_code: int = 500
    default_message: str = "Um erro ocorreu no servidor"
    
    def __init__(
        self,
        message: Optional[str] = None,
        status_code: Optional[int] = None,
        detail: Optional[Dict[str, Any]] = None
    ) -> None:
        self.message = message or self.default_message
        self.status_code = status_code or self.status_code
        self.detail = detail or {}
        super().__init__(self.message)

class AuthenticationException(APIException):
    """Erro ao autenticar usuário."""
    
    status_code = 401
    default_message = "Falha na autenticação"


class AuthorizationException(APIException):
    """Usuário não tem permissão para acessar o recurso."""
    
    status_code = 403
    default_message = "Você não tem permissão para acessar este recurso"


class StaffOnlyException(AuthorizationException):
    """Apenas funcionários podem acessar este recurso."""
    
    status_code = 403
    default_message = "Apenas funcionários podem realizar esta ação"


class OwnerAccessOnlyException(AuthorizationException):
    """Usuário só pode acessar seus próprios recursos."""
    
    status_code = 403
    default_message = "Você pode apenas acessar seus próprios pets"

class ResourceNotFoundException(APIException):
    """Recurso solicitado não foi encontrado."""
    
    status_code = 404
    default_message = "Recurso não encontrado"


class PetNotFoundException(ResourceNotFoundException):
    """Pet não encontrado."""
    
    status_code = 404
    default_message = "Pet não encontrado"


class VaccineNotFoundException(ResourceNotFoundException):
    """Vacina não encontrada."""
    
    status_code = 404
    default_message = "Vacina não encontrada"


class UserProfileNotFoundException(ResourceNotFoundException):
    """Perfil de usuário não encontrado."""
    
    status_code = 404
    default_message = "Perfil de usuário não encontrado"

class ValidationException(APIException):
    """Dados inválidos fornecidos."""
    
    status_code = 400
    default_message = "Dados inválidos"


class InvalidPetDataException(ValidationException):
    """Dados inválidos para pet."""
    
    status_code = 400
    default_message = "Dados inválidos para pet"


class InvalidVaccineDataException(ValidationException):
    """Dados inválidos para vacina."""
    
    status_code = 400
    default_message = "Dados inválidos para vacina"


class DuplicateResourceException(ValidationException):
    """Recurso duplicado (ex: CPF já existe)."""
    
    status_code = 409
    default_message = "Recurso duplicado"

class BusinessLogicException(APIException):
    """Violação de regra de negócio."""
    
    status_code = 400
    default_message = "Operação viola regra de negócio"


class VaccinationLogicException(BusinessLogicException):
    """Erro em lógica de vacinação."""
    
    status_code = 400
    default_message = "Erro ao processar vacinação"

class InternalServerException(APIException):
    """Erro interno não tratado."""
    
    status_code = 500
    default_message = "Erro interno do servidor"
