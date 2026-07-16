# v0.2.003 — Projects Domain Migration

## Mouse IA — Architecture Alignment

**Release:** v0.2  
**Task:** 003  
**Status:** Planned  
**Tipo:** Arquitetura / Migração de Domínio

---

# Objetivo

Migrar a entidade atual `Site` para a entidade oficial `Project`, corrigindo a duplicidade conceitual existente no modelo atual.

Esta task cria a camada intermediária oficial entre Organization e Asset, permitindo que o Mouse IA evolua para uma arquitetura de gerenciamento de superfície de ataque (ASM) escalável.

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

A implementação atual utiliza a entidade:

```text
Site
```

como uma entidade híbrida.

Ela possui duas responsabilidades diferentes:

## Container Operacional

Agrupa:

- ativos;
- scans;
- sinais;
- histórico operacional.

## Recurso Técnico

Armazena:

- URL;
- domínio;
- alvo utilizado pelo Scan Engine.

---

# Problema Identificado

A entidade Site viola o princípio de responsabilidade única.

Exemplo atual:

```text
Company

    |

  Site

    |

  Asset

    |

  Scan
```

Neste modelo:

- um Site representa um ambiente;
- um Site também representa um ativo técnico;
- novos tipos de ativos ficam limitados.

Exemplos futuros:

Um mesmo projeto pode possuir:

```text
Project

 ├── Website
 ├── API
 ├── IP Público
 ├── Aplicação Mobile
 ├── Repositório Git
 └── Cloud Resource
```

O modelo atual não suporta essa evolução corretamente.

---

# Decisão Arquitetural

Conforme definido na ADR-014:

A entidade Site deixa de existir como entidade de domínio.

Cada registro legado de Site será convertido em:

```text
Site legado

        ↓

Project

        +

Asset técnico correspondente
```

---

# Responsabilidade do Project

Project representa o contexto operacional de segurança.

Ele é responsável por agrupar:

- ativos monitorados;
- execuções de scans;
- evidências;
- descobertas;
- vulnerabilidades;
- recomendações.

Project NÃO representa um ativo técnico.

---

# Modelo de Domínio Alvo

Após a migração:

```text
Organization

        |

     Project

        |

      Asset

        |

      Scan
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


Project
1
|
N
Scan


Asset
1
|
N
Scan
```

---

# Migração de Dados

## Origem

Tabela atual:

```text
sites
```

Exemplo:

```json
{
"id": 1,
"name": "HMJ Fotografia",
"url": "https://hmjfotografia.com/",
"company_id": 1
}
```

---

# Destino

## Project

Será criado mantendo o mesmo identificador sempre que possível.

Exemplo:

```json
{
"id": 1,
"name": "HMJ Fotografia",
"description": "Projeto migrado do Site legado",
"organization_id": 1
}
```

---

## Asset

Será criado automaticamente representando o recurso técnico.

Exemplo:

```json
{
"id": 1,
"project_id": 1,
"name": "HMJ Fotografia Web Application",
"asset_type": "web_application",
"value": "https://hmjfotografia.com/",
"description": "Ativo criado automaticamente durante migração",
"is_active": true
}
```

---

# Preservação Histórica

A migração deverá preservar:

- IDs existentes quando possível;
- datas de criação;
- histórico de scans;
- sinais coletados;
- findings;
- vulnerabilidades;
- recomendações.

Nenhuma evidência de segurança poderá ser perdida.

---

# Alterações de Banco de Dados

## Antes

```text
sites

id
company_id
name
url
description
created_at
updated_at
```

---

## Depois

```text
projects

id
organization_id
name
description
created_at
updated_at
```

---

# Remoção do Campo URL

O campo:

```text
sites.url
```

não pertence ao Project.

Após migração:

```text
Project

↓

Asset.value
```

O endereço técnico passa a ser responsabilidade do Asset.

---

# Alterações Backend

Arquivos esperados:

## Models

Antes:

```text
site.py
```

Depois:

```text
project.py
```

Classe:

```python
Site

↓

Project
```

---

## Schemas

Antes:

```text
SiteCreate
SiteOut
SiteUpdate
```

Depois:

```text
ProjectCreate
ProjectOut
ProjectUpdate
```

---

## Repository

Antes:

```text
site_repository.py
```

Depois:

```text
project_repository.py
```

Responsabilidade:

- CRUD de Projects;
- filtros por Organization;
- validação multi-tenant.

---

## Service

Antes:

```text
site_service.py
```

Depois:

```text
project_service.py
```

---

## API

Antes:

```http
/sites
```

Depois:

```http
/projects
```

---

# Alterações Frontend

Alterações esperadas:

Antes:

```text
Sites.jsx
```

Depois:

```text
Projects.jsx
```

Mudanças:

- remover linguagem de site;
- exibir projetos;
- exibir assets associados;
- consumir endpoint /projects.

---

# Segurança Multi-Tenant

Todo Project obrigatoriamente pertence a uma Organization.

Regra:

```text
Usuário autenticado

        |

Organization permitida

        |

Project autorizado
```

Nunca permitir:

```text
Usuário A

consultar

Project da Organization B
```

---

# Estratégia de Implementação

A migração deverá seguir:

```text
1. Criar tabela projects

        ↓

2. Copiar sites para projects

        ↓

3. Criar assets derivados

        ↓

4. Atualizar relacionamentos

        ↓

5. Validar integridade

        ↓

6. Migrar consumidores
```

---

# Rollback

Antes da migração:

Obrigatório:

- backup completo;
- snapshot do banco;
- registro de execução.

Em caso de falha:

- restaurar banco anterior;
- remover estruturas criadas;
- manter relatório do erro.

---

# Testes Necessários

Atualizar:

Antes:

```text
test_sites.py
test_sites_auth.py
```

Depois:

```text
test_projects.py
test_projects_auth.py
```

Validar:

- criação de Projects;
- atualização;
- exclusão lógica;
- isolamento por Organization;
- associação de Assets.

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Domínio

- Site removido como entidade oficial;
- Project criado como container operacional;
- Asset separado como recurso técnico.

---

## Banco

- Projects existentes;
- Sites migrados;
- Assets derivados criados;
- Relacionamentos preservados.

---

## Segurança

- Project pertence obrigatoriamente a Organization;
- Não existe acesso cross-tenant.

---

## Compatibilidade

- Histórico operacional preservado;
- Testes atualizados;
- APIs consistentes.

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md

002-organizations.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
004-assets.md

↓

005-multi-tenancy.md

↓

006-api-refactor.md
```

---

# Observação Final

A criação do conceito Project é a principal evolução arquitetural da Release v0.2.

Ela remove a ambiguidade existente na entidade Site e estabelece uma base adequada para crescimento da plataforma como solução Enterprise de Attack Surface Management.