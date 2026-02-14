"""
Configuração centralizada de logging da aplicação.

Proporciona um sistema de logging padronizado para toda a aplicação.
"""

import logging
import logging.config
from pathlib import Path
from typing import Optional

# Diretório de logs
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Configuração de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} | {asctime} | {name} | {funcName}:{lineno} | {message}",
            "style": "{",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} | {asctime} | {name} | {message}",
            "style": "{",
            "datefmt": "%d/%m/%Y %H:%M:%S",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(timestamp)s %(level)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "vacina_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "vacinas.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file", "error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "clinica": {
            "handlers": ["console", "file", "vacina_file"],
            "level": "INFO",
            "propagate": False,
        },
        "usuarios": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}


def configure_logging() -> None:
    """Configura o logging da aplicação."""
    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger configurado.
    
    Args:
        name: Nome do logger (geralmente __name__ do módulo)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


# Loggers específicos por domínio
class DomainLoggers:
    """Loggers configurados para diferentes domínios."""
    
    @staticmethod
    def get_vacina_logger() -> logging.Logger:
        """Logger para operações de vacinação."""
        return get_logger("clinica.vacinas")
    
    @staticmethod
    def get_pet_logger() -> logging.Logger:
        """Logger para operações de pets."""
        return get_logger("clinica.pets")
    
    @staticmethod
    def get_auth_logger() -> logging.Logger:
        """Logger para operações de autenticação."""
        return get_logger("usuarios.auth")
    
    @staticmethod
    def get_perfil_logger() -> logging.Logger:
        """Logger para operações de perfis."""
        return get_logger("usuarios.perfis")
