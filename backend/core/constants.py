"""
Arquivo de constantes globais da aplicação.

Define valores mágicos e configurações reutilizáveis em todo o projeto.
Seguindo princípio de Clean Code: DRY (Don't Repeat Yourself).
"""

# ============================================================================
# Constantes de Vacinação
# ============================================================================
class VACCINATION_CONSTANTS:
    """Constantes relacionadas a vacinação e doses."""
    
    # Dias para próxima dose ser considerada "vencida"
    DAYS_UNTIL_OVERDUE = 0
    
    # Dias para próxima dose ser considerada "próxima em breve"
    DAYS_WARNING_THRESHOLD = 7
    
    # Dias para considerar animal como "em dia" com vacinação
    DAYS_UP_TO_DATE = 8
    
    # Intervalo padrão anual em dias
    DEFAULT_ANNUAL_INTERVAL_DAYS = 365


class VACCINATION_STATUS:
    """Valores de status de vacinação."""
    
    UP_TO_DATE = "em_dia"
    COMING_SOON = "proxima_em_breve"
    OVERDUE = "vencida"
    UNDEFINED = "indefinido"
    
    CHOICES = [
        (UP_TO_DATE, "Em dia"),
        (COMING_SOON, "Próxima em breve"),
        (OVERDUE, "Vencida"),
        (UNDEFINED, "Indefinido"),
    ]


# ============================================================================
# Constantes de Usuários e Perfis
# ============================================================================
class USER_ROLES:
    """Papéis/funções de usuário no sistema."""
    
    OWNER = "owner"  # Dono de pets
    STAFF = "staff"  # Funcionário/Veterinário
    ADMIN = "admin"  # Administrador


# ============================================================================
# Constantes de Mensagens
# ============================================================================
class ERROR_MESSAGES:
    """Mensagens de erro padronizadas."""
    
    PERMISSION_DENIED = "Você não tem permissão para acessar este recurso."
    OWNER_ACCESS_ONLY = "Você pode apenas acessar seus próprios pets."
    OWN_PETS_ONLY = "Você pode apenas criar pets para si mesmo."
    OWN_PETS_EDIT = "Você pode apenas editar seus próprios pets."
    OWN_PETS_DELETE = "Você pode apenas deletar seus próprios pets."
    STAFF_ONLY = "Apenas funcionários podem realizar esta ação."
    OWNER_PROFILE_NOT_FOUND = "Usuário não possui um perfil de dono."
    OWNER_NOT_FOUND = "Proprietário do pet não encontrado."
    ITEM_NOT_FOUND = "{model} com ID {id} não encontrado."


class SUCCESS_MESSAGES:
    """Mensagens de sucesso padronizadas."""
    
    ITEM_CREATED = "{model} criado com sucesso."
    ITEM_UPDATED = "{model} atualizado com sucesso."
    ITEM_DELETED = "{model} deletado com sucesso."


# ============================================================================
# Constantes de Validação
# ============================================================================
class VALIDATION_CONSTRAINTS:
    """Restrições e limites para validação."""
    
    MIN_PET_WEIGHT = 0.01
    MAX_PET_WEIGHT = 300.0
    MIN_VACCINE_PRICE = 0.01
    MAX_VACCINE_PRICE = 100000.0
    CPF_LENGTH = 11
    MIN_PASSWORD_LENGTH = 8
    MAX_USERNAME_LENGTH = 150
    MAX_NAME_LENGTH = 150


# ============================================================================
# Constantes de Paginação
# ============================================================================
class PAGINATION_CONSTANTS:
    """Constantes para paginação de APIs."""
    
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100


# ============================================================================
# Constantes de API
# ============================================================================
class API_TAGS:
    """Tags para documentação Swagger."""
    
    PETS = "Pets"
    PETS_VACCINATION = "Pets - Vacinação"
    VACCINES = "Vacinas"
    VACCINATION_HISTORY = "Histórico de Vacinação"
    STAFF_REPORTS = "Relatórios - Staff"
    AUTHENTICATION = "Autenticação"
    USERS = "Usuários"
    PROFILES = "Perfis"


# ============================================================================
# Constantes de JWT
# ============================================================================
class JWT_CONSTANTS:
    """Constantes relacionadas a JWT."""
    
    ACCESS_TOKEN_LIFETIME_MINUTES = 15
    REFRESH_TOKEN_LIFETIME_DAYS = 1
