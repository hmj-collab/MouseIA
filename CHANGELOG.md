# Changelog

Todas as mudanças relevantes do projeto Mouse IA serão documentadas neste arquivo seguindo o formato Keep a Changelog.

## [Unreleased]

### Added
- estrutura funcional inicial do backend com FastAPI
- CRUD do módulo de Sites com persistência em SQLite
- integração com SQLAlchemy e Alembic
- autenticação JWT com expiração e suporte a Bearer token
- autorização por papéis `admin` e `viewer` nas rotas protegidas
- módulos de Signals e Findings com modelos, schemas, repositórios, serviços, APIs e migrações
- interface estática de teste para login, Sites e Signals
- testes automatizados para health, autenticação, autorização, Sites, Signals e Findings
- documentação raiz atualizada para refletir o estado atual do projeto

### Changed
- documentação base e arquitetura refinadas para incluir autenticação, autorização, Signals e Findings

### Planned
- atualizações, exclusões e filtros para Signals e Findings
- fluxo automatizado de scans, coleta e correlação de sinais
- frontend integrado além da interface estática de teste

## [0.1.0] - 2026-07-16

### Added
- criação do repositório Mouse IA
- documentação inicial de visão geral e contexto do projeto
- arquivos base de documentação institucional
- estrutura inicial de diretórios para backend e frontend

### Changed
- reorganização da documentação para alinhar o projeto à visão de plataforma de segurança e vulnerabilidades

### Notes
- o projeto ainda está em fase inicial de desenvolvimento
- o foco atual é a construção da base arquitetural e da estrutura inicial para o módulo de Sites
