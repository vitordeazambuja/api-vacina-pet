"""
Tratamento centralizado de exceções.

Middleware que converte exceções da aplicação em respostas HTTP apropriadas.
"""

from typing import Optional, Dict, Any
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException as DRFAPIException
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied

from core.exceptions import APIException
from core.logging_config import get_logger

logger = get_logger(__name__)


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Optional[Response]:
    """
    Handler centralizado para exceções.
    
    Converte exceções da aplicação em respostas HTTP padronizadas.
    
    Args:
        exc: Exceção capturada
        context: Contexto da requisição
        
    Returns:
        Response com erro formatado ou None para deixar DRF tratar
    """
    
    # Tratar exceções customizadas da aplicação
    if isinstance(exc, APIException):
        return handle_api_exception(exc)
    
    # Tratar PermissionDenied do Django Core
    if isinstance(exc, DjangoPermissionDenied):
        return Response(
            {
                "error": "PermissionDenied",
                "message": str(exc) if str(exc) else "Você não tem permissão para executar esta ação.",
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Deixar DRF tratar suas próprias exceções
    if isinstance(exc, DRFAPIException):
        return exception_handler(exc, context)
    
    # Logar exceções não tratadas
    logger.error(
        f"Exceção não tratada: {type(exc).__name__}",
        exc_info=True,
        extra={"view": context.get("view"), "request": context.get("request")}
    )
    
    # Retornar erro genérico em produção
    return Response(
        {
            "error": "Erro interno do servidor",
            "detail": "Um erro inesperado ocorreu. Por favor, tente novamente mais tarde."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def handle_api_exception(exc: APIException) -> Response:
    """
    Trata exceção customizada da API.
    
    Args:
        exc: Exceção APIException
        
    Returns:
        Response formatada
    """
    
    # Mapear status code da exceção para HTTP
    http_status = exc.status_code
    
    # Construir corpo da resposta
    response_data = {
        "error": exc.__class__.__name__,
        "message": exc.message,
    }
    
    # Adicionar detalhes se disponíveis
    if exc.detail:
        response_data["detail"] = exc.detail
    
    # Logar erro conforme severidade
    if http_status >= 500:
        logger.error(f"Erro servidor: {exc.__class__.__name__} - {exc.message}")
    elif http_status >= 400:
        logger.warning(f"Erro cliente: {exc.__class__.__name__} - {exc.message}")
    
    return Response(response_data, status=http_status)


class ExceptionHandlingMiddleware:
    """
    Middleware (classe ASGI) para tratamento centralizado de exceções.
    
    Pode ser usado em aplicações ASGI alternativas ao padrão DRF.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except APIException as exc:
            logger.error(f"APIException capturada no middleware: {exc.message}")
            response = Response(
                {
                    "error": exc.__class__.__name__,
                    "message": exc.message,
                    "detail": exc.detail
                },
                status=exc.status_code
            )
        except DjangoPermissionDenied as exc:
            logger.warning(f"PermissionDenied capturada no middleware: {str(exc)}")
            response = Response(
                {
                    "error": "PermissionDenied",
                    "message": str(exc) if str(exc) else "Você não tem permissão para executar esta ação."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as exc:
            logger.error(f"Exceção não tratada capturada: {type(exc).__name__}", exc_info=True)
            response = Response(
                {
                    "error": "InternalServerError",
                    "message": "Um erro inesperado ocorreu"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return response