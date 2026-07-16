# Changelog

Todas as mudanças relevantes do projeto Mouse IA serão documentadas neste arquivo seguindo o formato Keep a Changelog.

## [Unreleased]

### Added
- CRUD completo do módulo de Empresas (`companies`) integrado às rotas e persistência.
- CRUD completo do módulo de Ativos (`assets`) e Varreduras (`scans`) com controle de papéis (`admin`/`viewer`).
- Motor de varredura síncrona no serviço de `scans` que analisa cabeçalhos HTTP (Server, X-Powered-By, HSTS, X-Frame-Options, CSP) e presença de assinaturas WordPress.
- Mecanismo de *offline fallback* no motor de scans para viabilizar testes e execuções em desenvolvimento local.
- Integração encadeada automática no pipeline: Varredura ➔ Geração de Sinais (`Signals`) ➔ Geração de Achados (`Findings`).
- Pacote `app.models` centralizando os modelos SQLAlchemy para evitar erros de tabelas referenciadas ausentes (`NoReferencedTableError`).
- Suporte a migrações em lote (`render_as_batch=True`) no Alembic para permitir modificações de colunas e constraints no SQLite.
- Testes automatizados cobrindo CRUD e regras de acesso de Empresas, Ativos, Scans e o pipeline de execução completa (subindo de 15 para 20 testes com 100% de sucesso).
- Frontend moderno (Single Page Application) em Vite + React + Lucide Icons construído com CSS customizado (sem Tailwind), contendo Dashboard interativo, gestão de escopo, gerenciamento de ativos/scans e painel de análise de ameaças.

### Changed
- Registro da rota `/companies` ativado em `main.py`.
- Configuração do template do Alembic (`script.py.mako`) corrigida para incluir definições explícitas de chaves de revisão.
- Ajuste nas configurações de CORS no backend para permitir solicitações de origem cruzada a partir do porto `5173` do Vite.

### Planned
- atualizações, exclusões e filtros avançados para Signals e Findings.
- motor de correlação (Fase 3) e enriquecimento de vulnerabilidades (CVE/NVD/CISA KEV/EPSS).
- suporte assíncrono para scans pesados por meio de filas (Celery/Redis).

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
