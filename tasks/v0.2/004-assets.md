# v0.2.004 — Assets Domain Migration

## Mouse IA — Architecture Alignment

**Release:** v0.2  
**Task:** 004  
**Status:** Planned  
**Tipo:** Arquitetura / Migração de Domínio

---

# Objetivo

Migrar a entidade `Asset` para o novo modelo de domínio baseado em `Project`, removendo o acoplamento existente com `Site` e consolidando o conceito de ativo monitorado como entidade independente.

Esta task estabelece a base para evolução do Mouse IA como plataforma de Attack Surface Management (ASM).

---

# Documentos de Referência

Esta task deve respeitar:

- ARCHITECTURE.md
- AGENT.md
- DOMAIN.md
- DECISIONS.md
- SECURITY.md
- PLANO_DE_MIGRAÇÃO_ARQUITETURAL.md

Decisões relacionadas:

- ADR-010 — Documentação como Fonte de Verdade
- ADR-011 — Isolamento Multi-Tenant por Organization
- ADR-014 — Separação de Containers Operacionais e Recursos Monitorados

---

# Contexto Atual

A implementação atual possui Assets vinculados diretamente à entidade Site.

Modelo atual:

```text
Company

    |

 Site

    |

 Asset

    |

 Scan
```

O Asset depende do Site para existir dentro do escopo operacional.

---

# Problema Identificado

O modelo atual limita a evolução da plataforma.

Um Site representa apenas uma pequena parte da superfície de ataque.

Em ambientes reais, uma organização possui diversos tipos de ativos:

Exemplo:

```text
Empresa

    |

Projeto Segurança Externo

    |

    ├── website.com.br
    ├── api.website.com.br
    ├── 200.10.20.30
    ├── aplicativo mobile
    ├── repositório Git
    └── serviço cloud
```

O conceito de Asset precisa existir independentemente de um website.

---

# Decisão Arquitetural

Asset será tratado como recurso técnico monitorado.

A responsabilidade do Asset será:

- representar um alvo técnico;
- possuir identificação própria;
- armazenar características técnicas;
- receber scans;
- gerar Signals.

O Asset NÃO representa contexto operacional.

O contexto operacional pertence ao Project.

---

# Modelo de Domínio Alvo

Após migração:

```text
Organization

        |

     Project

        |

      Asset

        |

      Scan

        |

     Signal
```

Relacionamentos:

```text
Organization
1
|
N
Project


Project
1
|
N
Asset


Asset
1
|
N
Scan


Asset
1
|
N
Signal
```

---

# Tipos de Assets

A arquitetura deverá permitir diferentes categorias de ativos.

Exemplos:

```text
web_application

domain

subdomain

ip_address

api

repository

cloud_resource

mobile_application
```

Novos tipos poderão ser adicionados sem alteração estrutural do domínio.

---

# Migração de Dados

## Estado Atual

Exemplo:

```json
{
"id": 1,
"site_id": 1,
"name": "HMJ Fotografia",
"url": "https://hmjfotografia.com/"
}
```

---

# Estado Alvo

Após migração:

```json
{
"id": 1,
"project_id": 1,
"name": "HMJ Fotografia Web Application",
"asset_type": "web_application",
"value": "https://hmjfotografia.com/",
"description": "Ativo criado a partir do Site legado",
"is_active": true
}
```

---

# Alterações de Banco de Dados

## Antes

Tabela:

```text
assets
```

Relacionamento:

```text
asset.site_id
```

---

## Depois

Tabela:

```text
assets
```

Relacionamento:

```text
asset.project_id
```

---

# Remoção de Acoplamentos

Remover:

```text
company_id
```

quando existente.

Remover:

```text
site_id
```

como relacionamento principal.

Adicionar:

```text
project_id
```

obrigatório.

---

# Regras de Integridade

Todo Asset deve possuir:

Obrigatório:

```text
project_id
name
asset_type
value
```

---

Um Asset nunca deve existir fora de um Project.

Regra:

```text
Organization

↓

Project

↓

Asset
```

---

# Alterações Backend

## Models

Arquivo:

```text
asset.py
```

Alterações:

Antes:

```python
site_id
```

Depois:

```python
project_id
```

---

## Schemas

Atualizar:

```text
AssetCreate
AssetOut
AssetUpdate
```

Incluindo:

```text
project_id
asset_type
value
```

---

## Repository

Arquivo:

```text
asset_repository.py
```

Alterar filtros:

Antes:

```text
site_id
```

Depois:

```text
project_id
```

Garantir validação de Organization através do Project.

---

## Service

Arquivo:

```text
asset_service.py
```

Responsabilidades:

- criação de Assets;
- validação de Project;
- controle de escopo;
- regras de negócio.

---

## API

Endpoints existentes:

```http
/assets
```

serão mantidos.

Porém:

Payloads deverão utilizar:

```json
{
"project_id": 1,
"name": "API Principal",
"asset_type": "api",
"value": "https://api.exemplo.com"
}
```

---

# Alterações Frontend

Componentes impactados:

- Assets;
- Projects;
- Dashboard;
- Scans.

Alterações:

Antes:

```text
Selecionar Site
```

Depois:

```text
Selecionar Project

↓

Selecionar Asset
```

---

# Scan Engine

O Scan Engine deverá deixar de buscar alvos diretamente no Site.

Antes:

```text
Scan

↓

Site.url
```

Depois:

```text
Scan

↓

Asset.value
```

---

# Preservação Histórica

Nenhum histórico deverá ser perdido.

Preservar:

- Assets existentes;
- Scans;
- Signals;
- Findings;
- Vulnerabilidades;
- Recomendações.

---

# Estratégia de Implementação

A execução deverá seguir:

```text
1. Criar relacionamento project_id

        ↓

2. Migrar Assets existentes

        ↓

3. Validar integridade

        ↓

4. Atualizar Services

        ↓

5. Atualizar APIs

        ↓

6. Remover dependências antigas
```

---

# Rollback

Antes da alteração:

Obrigatório:

- backup;
- snapshot;
- registro da migration.

Caso ocorra falha:

- restaurar banco;
- remover estruturas novas;
- validar consistência.

---

# Testes Necessários

Atualizar:

```text
test_assets.py

test_assets_scans.py
```

Validar:

- criação de Asset;
- associação com Project;
- isolamento por Organization;
- execução de Scan;
- geração de Signals.

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Domínio

- Asset não depender de Site;
- Asset pertencer exclusivamente a Project;
- Asset representar recurso técnico.

---

## Banco

- project_id implementado;
- relacionamentos atualizados;
- dados preservados.

---

## Segurança

- Assets respeitam isolamento multi-tenant;
- nenhum Asset acessível fora da Organization.

---

## Evolução

Novo modelo permite:

- múltiplos Assets por Project;
- novos tipos de ativos;
- expansão ASM.

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md

002-organizations.md

003-projects.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
005-multi-tenancy.md

↓

006-api-refactor.md

↓

007-data-migration.md
```

---

# Observação Final

A migração de Asset representa a transformação do Mouse IA de um scanner orientado a websites para uma plataforma de gerenciamento de superfície de ataque.

O Asset passa a ser o elemento técnico central da coleta de segurança, enquanto Project assume exclusivamente o papel de organização operacional.