# API Clínica Veterinária - Sistema de Vacinação

### Desenvolvido para o Processo Seletivo - Desenvolvedor Backend Junior | IVARE

## Sobre o Projeto

API RESTful para **gestão de vacinação de pets** em clínicas veterinárias. Implementa princípios de **Clean Code** e **Clean Architecture** com separação clara de responsabilidades em camadas e boas práticas.

### Destaques do Projeto

| **Diferencial**             | **Descrição**                                                   |
| :-------------------------- | :-------------------------------------------------------------- |
| **Clean Architecture**      | Separação em camadas (Views → Services → Repositories → Models) |
| **Docker Ready**            | Ambiente completo containerizado com Docker Compose             |
| **Logging Estruturado**     | Sistema de logs por domínio com níveis configuráveis            |
| **Autenticação JWT**        | Tokens stateless para autenticação segura                       |
| **Documentação Automática** | Swagger integrado via drf-spectacular                           |
| **Testes Unitários**        | Cobertura de testes para modelos principais                     |
| **Type Hints 100%**         | Type annotations completas em Services                          |
| **Insomnia Collection**     | Fluxo completo de requisições pré-configurado                   |

### Funcionalidades Principais

- **Gestão de Pets** - CRUD completo com validações e isolamento por proprietário
- **Catálogo de Vacinas** - Gerenciamento de vacinas disponíveis (apenas funcionários)
- **Histórico de Vacinação** - Registro e acompanhamento de doses aplicadas
- **Alertas Inteligentes** - Notificação de doses próximas e vencidas
- **Controle de Acesso** - Permissões diferenciadas por perfil (Dono/Funcionário)

---

### Pré-requisitos

- Docker e Docker Compose
  **OU**
- Python e pip

### Opção 1: Docker

```bash
# Clone o repositório
git clone https://github.com/vitordeazambuja/api-vacina-pet.git
cd api-vacina-pet

# Configure variáveis de ambiente
make env

# Inicie os containers
make build

# Execute as migrações
make migrate

# Crie um superusuário (Opcional)
make superuser
```

**Pronto!** A API estará rodando em `http://localhost:8000`

### Opção 2: Python Local

```bash
# Clone o repositório
git clone https://github.com/vitordeazambuja/api-vacina-pet.git
cd api-vacina-pet

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cd backend
cp .env.example .env

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

---

## Documentação da API

### Interfaces Disponíveis

| Interface        | URL                               | Descrição                        |
| :--------------- | :-------------------------------- | :------------------------------- |
| **Swagger UI**   | `http://localhost:8000/api/docs/` | Documentação interativa completa |
| **Admin Django** | `http://localhost:8000/admin/`    | Painel administrativo            |

### Como Testar a API

#### **Método 1: Insomnia**

1. Importe o arquivo `InsomniaImport.json` no Insomnia
2. Execute o **Fluxo Completo Automatizado** que inclui:
   - Criação de usuários (Dono + Funcionário)
   - Autenticação JWT
   - Cadastro de Pet
   - Registro de Vacina
   - Aplicação de Vacinação
   - Consulta de Histórico

> Tudo já está configurado, as variáveis são setadas automaticamente entre as requisições do fluxo.

#### **Método 2: Swagger UI**

Acesse `http://localhost:8000/api/docs/` e teste diretamente pelo navegador.

---

## Arquitetura

### Estrutura em Camadas (Clean Architecture)

```
┌─────────────────────────────────────────────────────────┐
│                    HTTP / REST Layer                    │
│              (Views/ViewSets - Apresentação)            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Serializers Layer                      │
│              (DTOs - Validação e Serialização)          │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   Services Layer                        │
│                 LÓGICA DE NEGÓCIO                       │
│  • PetService                                           │
│  • VaccinationService                                   │
│  • Validações complexas                                 │
│  • Logging integrado                                    │
│  • Exceções customizadas                                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                 Repositories Layer                      │
│                 ACESSO A DADOS                          │
│  • PetRepository                                        │
│  • VaccineRepository                                    │
│  • VaccinationRepository                                │
│  • Abstração de queries                                 │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                    Models Layer                         │
│                (ORM + Banco de Dados)                   │
└─────────────────────────────────────────────────────────┘
```

### Estrutura de Diretórios

```
api-vacina-pet/
├── docker-compose.yml        # Orquestração de containers
├── Dockerfile                # Imagem Python
├── Makefile                  # Comandos automatizados
├── requirements.txt          # Dependências Python
├── InsomniaImport.json       # Collection completa
│
└── backend/
    ├── core/                    # Infraestrutura Central
    │   ├── constants.py         # Constantes globais
    │   ├── exceptions.py        # Exceções customizadas
    │   ├── logging_config.py    # Sistema de logs
    │   ├── exception_handler.py # Handler centralizado
    │   └── settings.py          # Configurações Django
    │
    ├── clinica/                 # App Principal
    │   ├── models.py            # Pet | Vacina | PetVacina
    │   ├── views.py             # ViewSets (camada HTTP)
    │   ├── serializers.py       # DTOs
    │   ├── tests.py             # Testes unitários
    │   │
    │   ├── services/            # Lógica de Negócio
    │   │   ├── pet_service.py
    │   │   └── vaccination_service.py
    │   │
    │   └── repositories/        # Camada de Dados
    │       ├── pet_repository.py
    │       ├── vaccine_repository.py
    │       └── vaccination_repository.py
    │
    └── usuarios/                # Autenticação
        ├── models.py            # Usuario | PerfilDono | PerfilFuncionario
        └── ...
```

---

## Principais Endpoints

### Autenticação

```http
POST   /api/v1/auth/token/           # Obter token JWT
POST   /api/v1/auth/token/refresh/   # Renovar token
POST   /api/v1/auth/usuarios/        # Criar usuário
```

### Pets

```http
GET    /api/v1/clinica/pets/                         # Listar pets
POST   /api/v1/clinica/pets/                         # Criar pet
GET    /api/v1/clinica/pets/{id}/                    # Detalhes do pet
PATCH  /api/v1/clinica/pets/{id}/                    # Atualizar pet
DELETE /api/v1/clinica/pets/{id}/                    # Deletar pet
GET    /api/v1/clinica/pets/{id}/historico_vacinas/  # Histórico de vacinação
```

### Vacinas

```http
GET    /api/v1/clinica/vacinas/        # Listar vacinas
POST   /api/v1/clinica/vacinas/        # Criar vacina (apenas funcionários)
GET    /api/v1/clinica/vacinas/{id}/   # Detalhes da vacina
```

### Vacinação

```http
GET    /api/v1/clinica/pet-vacinas/                        # Listar vacinações
POST   /api/v1/clinica/pet-vacinas/                        # Registrar vacinação (apenas funcionários)
GET    /api/v1/clinica/pet-vacinas/proximas_doses_sistema/ # Próximas doses
GET    /api/v1/clinica/pet-vacinas/doses_vencidas_sistema/ # Doses vencidas
```

> **Documentação completa**: Acesse o Swagger em `/api/docs/` para ver todos os endpoints e modelos

---

### Destaques da Implementação

| Conceito                     | Implementação                                       |
| :--------------------------- | :-------------------------------------------------- |
| **Constantes Centralizadas** | `core/constants.py` - Zero magic strings/numbers    |
| **Exceções Customizadas**    | Hierarquia clara com exceções específicas           |
| **Logging por Domínio**      | Separação em `app.log`, `errors.log`, `vacinas.log` |
| **Type Hints 100%**          | Todos os métodos de Services tipados                |
| **Repository Pattern**       | Abstração completa do acesso a dados                |
| **Service Layer**            | Lógica de negócio isolada das Views                 |

---

## Stack

| Categoria           | Tecnologias                             |
| :------------------ | :-------------------------------------- |
| **Backend**         | Python / Django / Django REST Framework |
| **Autenticação**    | djangorestframework-simplejwt           |
| **Documentação**    | drf-spectacular (Swagger/ReDoc)         |
| **Banco de Dados**  | SQLite                                  |
| **Containerização** | Docker / Docker Compose                 |
| **Utilitários**     | python-dotenv / django-cors-headers     |
