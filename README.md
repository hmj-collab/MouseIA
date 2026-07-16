# Mouse IA

Mouse IA é uma plataforma modular para gestão inteligente de vulnerabilidades e superfícies de ataque. O projeto já passou da fase conceitual para uma base funcional de backend, com os módulos de Sites, Signals e Findings e a primeira camada de autenticação e autorização.

## Status atual

A base do projeto já está operacional localmente:

- backend FastAPI com endpoint de saúde
- CRUD de Sites com persistência em SQLite
- criação e consulta de Signals associados opcionalmente a Sites
- criação e consulta de Findings associados opcionalmente a Signals
- integração com SQLAlchemy e Alembic
- autenticação JWT e autorização baseada nos papéis `admin` e `viewer`
- interface estática de teste para login, Sites e Signals
- testes automatizados cobrindo health, autenticação, autorização, Sites, Signals e Findings

## Visão geral

A proposta do Mouse IA é apoiar equipes de segurança com:

- cadastro e gestão de ativos digitais
- coleta e organização de sinais e evidências
- correlação de risco e contexto operacional
- geração de achados, vulnerabilidades e recomendações
- acompanhamento de ações de remediação

O fluxo principal segue a direção:

Asset → Scan → Signals → Correlation Engine → Findings → Vulnerabilities → Recommendations → Tasks

## Requisitos do projeto

- Python 3.9 ou superior
- ambiente virtual com venv
- pip
- SQLite para desenvolvimento local
- PostgreSQL como alvo de produção futuro

## Stack atual

- FastAPI para APIs
- Pydantic para validação de dados
- SQLAlchemy para camada de persistência
- Alembic para migrações
- pytest para testes automatizados
- Uvicorn para execução local

## Como executar localmente

1. Entre na pasta do backend.
2. Crie e ative um ambiente virtual.
3. Instale as dependências necessárias.
4. Aplique as migrações.
5. Execute a aplicação localmente.

Exemplo prático:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]" pydantic-settings httpx sqlalchemy alembic pytest pytest-cov psycopg2-binary
alembic upgrade head
uvicorn app.main:app --reload
```

Em outro terminal, a interface de teste pode ser executada em `http://127.0.0.1:3000`:

```bash
cd frontend
npm start
```

Para o ambiente local, use `admin` ou `viewer` com a senha `password123` para obter um token. Essas credenciais são apenas de desenvolvimento.

## Estrutura do repositório

```text
backend/
  app/
    api/
    core/
    database/
    models/
    repositories/
    schemas/
    services/
  alembic/
  tests/
frontend/
  index.html
  package.json
docs/
scripts/
```

## Módulos em evolução

### Módulo de Sites

Já implementado em sua primeira versão funcional com CRUD, persistência, autenticação e testes.

### Módulos de Signals e Findings

Implementados em sua primeira versão com criação, consulta, persistência e vínculo opcional com Site e Signal, respectivamente. A correlação automática entre eles continua como evolução futura.

### Próximos módulos previstos

- Empresas
- Ativos
- Scans
- Vulnerabilidades
- Recomendações
- Tarefas

## Documentação relacionada

- [ARCHITECTURE.md](ARCHITECTURE.md): visão técnica e arquitetura da solução
- [ROADMAP.md](ROADMAP.md): evolução do projeto por fases
- [SECURITY.md](SECURITY.md): diretrizes de segurança
- [SIGNALS.md](SIGNALS.md): fluxo conceitual de sinais e análise
- [CHANGELOG.md](CHANGELOG.md): histórico de mudanças

## Próximos passos

As próximas etapas prioritárias são:

- evoluir o modelo de Sites para campos adicionais
- implementar os fluxos de atualização e exclusão de Signals e Findings
- implementar scans e correlação automática de sinais
- evoluir a interface de teste para um frontend integrado e completo

## Licença

Este projeto está sob a licença definida no arquivo LICENSE.
