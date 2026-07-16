# Arquitetura do Mouse IA

## 1. Visão geral

O Mouse IA é uma plataforma modular para gestão inteligente de vulnerabilidades e superfícies de ataque. O projeto saiu da fase de estrutura conceitual e já possui uma base funcional de backend com os módulos de Sites, Signals e Findings.

A proposta continua expandindo para integrações com GitHub, Azure DevOps, GitLab, Docker, Kubernetes, Nginx, Apache, IIS, Linux, Windows, Cloudflare, SSL e DNS.

## 2. Objetivo do projeto

Construir uma plataforma escalável, modular e orientada a inteligência artificial para:

- cadastrar e gerenciar ativos digitais
- coletar sinais e evidências de segurança
- correlacionar vulnerabilidades e riscos
- gerar achados, recomendações e tarefas
- apoiar decisões operacionais e estratégicas em segurança

## 3. Estado atual da implementação

A base atual já contempla:

- backend FastAPI estruturado e rotas ativas
- CRUD de Empresas (`companies`) com restrições de papéis
- CRUD de Sites com persistência em SQLite
- CRUD de Ativos (`assets`) e Varreduras (`scans`)
- Motor síncrono de varredura que analisa alvos HTTP, cabeçalhos expostos e assinaturas (WordPress)
- CRUD de Sinais (`signals`) e Achados (`findings`) gerados automaticamente de forma encadeada ou criados manualmente
- persistência unificada via SQLAlchemy carregando todos os modelos do pacote `app.models`
- migrações em lote com Alembic (`render_as_batch=True` para suporte a SQLite)
- autenticação JWT com os papéis `admin` e `viewer`
- autorização robusta com base em escopos/papéis em todas as rotas de domínio
- interface estática local simples para testes
- 20 testes automatizados cobrindo ponta a ponta todos os componentes atuais com 100% de sucesso

## 4. Princípios de arquitetura

- Modularidade: cada domínio deve ser isolado por responsabilidade
- Escalabilidade: a plataforma deve crescer por módulos sem acoplar tudo em uma única camada
- Observabilidade: o sistema deve permitir rastreio, logs e auditoria
- Segurança: autenticação, autorização e proteção de dados são fundamentais
- Extensibilidade: novos módulos e integrações devem ser adicionados com baixo impacto

## 5. Arquitetura em camadas

### Camada de apresentação

Responsável pela interface de usuário e interação com o sistema.

- frontend web
- dashboards e telas de gestão
- experiência para operação e análise

### Camada de aplicação

Responsável pela orquestração da lógica de negócio.

- APIs REST com FastAPI
- serviços de domínio
- casos de uso
- regras de negócio aplicadas ao contexto do módulo

### Camada de domínio

Responsável pelas regras e modelos centrais do negócio.

- entidades como sites, ambientes, sinais e vulnerabilidades
- validações de negócio
- fluxo de análise e correlação

### Camada de infraestrutura

Responsável por integração com tecnologias externas e persistência.

- banco de dados SQLite para desenvolvimento local
- PostgreSQL como alvo de produção
- migrations com Alembic
- filas assíncronas e cache no futuro

## 6. Estrutura do backend atual

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
```

## 7. Organização dos módulos

### Módulo de Sites

Responsável por cadastrar e gerenciar sites para auditoria. Atualmente já possui:

- criação
- leitura
- atualização
- exclusão
- persistência em banco

### Módulo de Signals

Responsável por registrar observações de segurança. Cada sinal possui origem, tipo, severidade, confiança, descrição e vínculo opcional com um Site.

### Módulo de Findings

Responsável por registrar achados estruturados. Cada achado possui título, descrição, severidade, status e vínculo opcional com um Signal.

### Módulos futuros

- Empresas
- Ativos
- Scans
- Vulnerabilidades
- Recomendações
- Tarefas

## 8. Requisitos técnicos atuais

- Python 3.9+
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- pytest
- SQLite para desenvolvimento local

## 9. APIs implementadas até o momento

### Gestão de empresas (Companies)

- POST /companies
- GET /companies
- GET /companies/{id}
- PUT /companies/{id}
- DELETE /companies/{id}

### Gestão de sites

- POST /sites
- GET /sites
- GET /sites/{id}
- PUT /sites/{id}
- DELETE /sites/{id}

### Gestão de ativos (Assets)

- POST /assets
- GET /assets
- GET /assets/{id}
- PUT /assets/{id}
- DELETE /assets/{id}

### Gestão de varreduras (Scans)

- POST /scans
- GET /scans
- GET /scans/{id}
- PUT /scans/{id}
- DELETE /scans/{id}
- POST /scans/{id}/launch (inicia a varredura e gera Sinais/Achados)

### Gestão de signals

- POST /signals
- GET /signals
- GET /signals/{id}

### Gestão de findings

- POST /findings
- GET /findings
- GET /findings/{id}

> [!NOTE]
> Para todas as entidades acima (exceto autenticação e saúde), a leitura (`GET`) aceita os papéis `admin` e `viewer`, enquanto a escrita/modificação (`POST`, `PUT`, `DELETE`, `launch`) exige privilégios de `admin`.

### Autenticação

- POST /auth/login
- POST /auth/register
- GET /protected

O login emite um token JWT Bearer com expiração de uma hora. Os usuários de desenvolvimento `admin` e `viewer` possuem, respectivamente, os papéis `admin` e `viewer`.

### Saúde do sistema

- GET /health

## 10. Próximos passos arquiteturais

- evoluir o modelo de Sites com mais atributos de contexto
- introduzir scans e correlação automática de sinais
- adicionar atualização e exclusão para Signals e Findings
- preparar a base para integração com frontend e serviços externos

A autenticação deve ser baseada em autenticação segura e escalável, com possibilidade de evolução para múltiplos provedores.

### Estratégia inicial

- autenticação por e-mail e senha
- uso de tokens JWT
- controle de permissões por papéis

### Evolução futura

- SSO
- integração com provedores corporativos
- autenticação multifator

## 13. Estratégia de filas

O sistema deve utilizar filas para processar operações pesadas de forma assíncrona.

### Cenário principal

- execução de scans
- processamento de sinais
- geração de findings e recomendações

### Tecnologia sugerida

- Celery ou equivalente
- integração com Redis ou broker semelhante

## 14. Estratégia de cache

Cache deve ser usado para reduzir latência e evitar consultas repetidas.

### Casos principais

- listas de empresas e sites
- configurações de ambiente
- dados estáticos ou pouco mutáveis

## 15. Estratégia de IA

A IA será utilizada como camada de apoio, não como substituto da análise humana.

### Casos de uso esperados

- resumo de achados
- classificação de riscos
- recomendação de ações
- suporte à triagem inicial

## 16. Estratégia de atualização das bases CVE/NVD

A plataforma deve manter bases externas atualizadas para enriquecer os achados.

### Estratégia proposta

- sincronização periódica com fontes públicas como NVD e CISA KEV
- armazenamento local para consulta rápida
- atualização em background
- versionamento e rastreio das mudanças

## 17. Estratégia de escalabilidade

A arquitetura deve crescer de forma incremental.

### Diretrizes

- separar módulos por domínio
- manter serviços desacoplados
- usar filas para processamento pesado
- aplicar observabilidade desde o início
- preparar a plataforma para multi-tenant e multi-ambiente

## 18. Roadmap de evolução

### Versão 1.0

- estrutura inicial do projeto
- backend com FastAPI
- banco PostgreSQL e migrations
- módulo de Sites
- CRUD básico

### Versão 1.1

- gestão de empresas e ambientes
- dashboard inicial
- autenticação básica
- API documentada

### Versão 2.0

- módulo de scans e sinais
- correlação de dados
- integração com fontes externas

### Versão 3.0

- IA para análise e recomendação
- relatórios avançados
- integração com infraestrutura e repositórios

## 19. Resumo executivo

O Mouse IA será uma plataforma modular de gestão de segurança e vulnerabilidades, iniciando com o cadastro e análise de sites e expandindo para um ecossistema mais amplo de observação e recomendação. A arquitetura proposta prioriza modularidade, escalabilidade, segurança e evolução incremental, alinhada ao plano descrito no prompt do projeto.
