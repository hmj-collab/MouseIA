# Arquitetura do Mouse IA

## 1. Visão geral

O Mouse IA é uma plataforma profissional de gestão inteligente de vulnerabilidades e superfícies de ataque. A proposta não é apenas realizar varreduras de WordPress, mas atuar como uma camada central de observação, análise e priorização de riscos para ativos digitais.

A plataforma será evoluída em módulos, começando com sites e expandindo para integrações com GitHub, Azure DevOps, GitLab, Docker, Kubernetes, Nginx, Apache, IIS, Linux, Windows, Cloudflare, SSL e DNS.

## 2. Objetivo do projeto

Construir uma plataforma escalável, modular e orientada a inteligência artificial para:

- cadastrar e gerenciar ativos digitais
- coletar sinais e evidências de segurança
- correlacionar vulnerabilidades e riscos
- gerar achados, recomendações e tarefas
- apoiar decisões operacionais e estratégicas em segurança

## 3. Escopo

### Escopo inicial

- gestão de sites para auditoria
- cadastro de empresas, ambientes e tecnologias
- estrutura base de API, banco de dados e módulos
- fluxo de criação, leitura, atualização e exclusão de entidades

### Escopo futuro

- scanners específicos por tecnologia
- integração com repositórios e ambientes de deployment
- análise de infraestrutura, DNS, SSL, cloud e servidores
- enriquecimento com inteligência artificial e bases externas como CVE, NVD, CISA KEV e EPSS

## 4. Princípios de arquitetura

- Modularidade: cada domínio deve ser isolado por responsabilidade
- Escalabilidade: a plataforma deve crescer por módulos, sem acoplar tudo em uma única camada
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

- APIs REST
- serviços de domínio
- casos de uso
- regras de negócio aplicadas ao contexto do módulo

### Camada de domínio

Responsável pelas regras e modelos centrais do negócio.

- entidades como empresas, sites, ambientes, sinais e vulnerabilidades
- validações de negócio
- fluxo de análise e correlação

### Camada de infraestrutura

Responsável por integração com tecnologias externas e persistência.

- banco de dados PostgreSQL
- migrations com Alembic
- filas assíncronas
- cache
- integrações com providers externos

## 6. Arquitetura funcional

O fluxo principal da plataforma segue a ideia de um pipeline de análise:

1. Cadastro de ativos e entidades
2. Coleta de sinais e evidências
3. Processamento e correlação
4. Geração de achados e vulnerabilidades
5. Criação de recomendações e tarefas

Fluxo resumido:

Asset → Scan → Signals → Correlation Engine → Findings → Vulnerabilities → Recommendations → Tasks

## 7. Estrutura de diretórios

```text
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   └── deps/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── security.py
│   │   └── settings.py
│   ├── database/
│   ├── domain/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── scanners/
│   ├── utils/
│   ├── workers/
│   └── main.py
├── alembic/
├── intel/
├── tests/
└── pyproject.toml

frontend/
├── app/
├── components/
├── lib/
├── public/
├── services/
└── types/

docker/
docs/
scripts/
```

## 8. Organização dos módulos

### Módulo de Sites

Responsável por cadastrar e gerenciar sites para auditoria.

Entidades principais:
- nome
- URL
- ambiente
- empresa
- categoria
- tecnologia
- status
- data de criação
- último scan
- score atual

### Módulo de Empresas

Responsável por representar organizações e seus contextos.

### Módulo de Ativos

Responsável por organizar recursos digitais associados a uma empresa.

### Módulo de Scans

Responsável por executar e registrar varreduras e coletas.

### Módulo de Sinais

Responsável por capturar evidências e eventos observados.

### Módulo de Findings

Responsável por consolidar resultados e evidências em achados estruturados.

### Módulo de Vulnerabilidades

Responsável por associar vulnerabilidades conhecidas e contextos de risco.

### Módulo de Recomendações

Responsável por gerar sugestões de remediação e ação.

### Módulo de Tarefas

Responsável por organizar a execução das recomendações.

## 9. Responsabilidades por camada

### Backend

- expor APIs para frontend e integrações
- implementar serviços e regras de negócio
- encapsular acesso a banco, filas e cache
- orquestrar scanners e processamento assíncrono

### Frontend

- oferecer telas de navegação e gestão
- apresentar dashboards e resultados
- consumir APIs e organizar a experiência do usuário

## 10. Modelagem de banco de dados

A base de dados deve ser organizada de forma relacional, com foco em rastreabilidade e evolução modular.

### Entidades principais

- Empresas
- Sites
- Ambientes
- Categorias
- Tecnologias
- Scans
- Sinais
- Findings
- Vulnerabilidades
- Recomendações
- Tarefas
- Usuários

### Relações esperadas

- uma empresa possui vários sites
- um site pertence a um ambiente e tecnologia
- um site pode ter vários scans
- um scan gera vários sinais
- um sinal pode originar um ou mais findings
- um finding pode se relacionar a uma ou mais vulnerabilidades
- uma recomendação pode gerar tarefas

## 11. APIs necessárias

### Gestão de sites

- POST /sites
- GET /sites
- GET /sites/{id}
- PUT /sites/{id}
- DELETE /sites/{id}

### Gestão de empresas

- POST /companies
- GET /companies
- GET /companies/{id}
- PUT /companies/{id}
- DELETE /companies/{id}

### Gestão de scans

- POST /scans
- GET /scans
- GET /scans/{id}

### Gestão de findings e vulnerabilidades

- GET /findings
- GET /findings/{id}
- GET /vulnerabilities
- GET /vulnerabilities/{id}

## 12. Estratégia de autenticação

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
