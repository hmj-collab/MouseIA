# v0.2.006 — API Refactor

## Mouse IA — Domain API Alignment

**Release:** v0.2  
**Task:** 006  
**Status:** Planned  
**Tipo:** Backend / API Contract Migration

---

# Objetivo

Adaptar a camada de APIs do Mouse IA para refletir o novo modelo de domínio definido na arquitetura oficial.

Esta task representa a transição dos contratos HTTP existentes para a nova estrutura baseada em:

```text
Organization

      |

   Project

      |

    Asset

      |

    Scan
```

---

# Princípio Fundamental

A API do Mouse IA deve seguir a premissa:

> Um cliente do Mouse IA nunca deve saber que outro cliente existe.

Toda operação deverá respeitar:

```text
Authentication

        |

Authorization

        |

Organization Isolation

        |

Resource Access
```

---

# Documentos de Referência

Esta task deve respeitar:

- ARCHITECTURE.md
- AGENT.md
- DOMAIN.md
- SECURITY.md
- DECISIONS.md
- PLANO_DE_MIGRAÇÃO_ARQUITETURAL.md

Decisões relacionadas:

- ADR-010 — Documentação como Fonte de Verdade
- ADR-011 — Isolamento Multi-Tenant
- ADR-014 — Separação entre Container e Recurso Monitorado

---

# Contexto Atual

A API atual foi construída seguindo o modelo inicial:

```text
Companies

Sites

Assets

Scans
```

Endpoints existentes:

```http
/companies

/sites

/assets

/scans
```

---

# Problema Identificado

Após a evolução do domínio, esses endpoints não representam mais corretamente a arquitetura.

Problemas:

- nomenclatura divergente;
- ausência de Projects;
- validações de tenant incompletas;
- payloads baseados em Site;
- acoplamento entre recurso técnico e container operacional.

---

# Novo Contrato de Domínio

A API deverá representar:

```text
Organization

        |

     Project

        |

      Asset

        |

      Scan
```

---

# Alterações de Endpoints

## Organizations

Antes:

```http
GET /companies

POST /companies

PUT /companies/{id}

DELETE /companies/{id}
```

Depois:

```http
GET /organizations

POST /organizations

PUT /organizations/{id}

DELETE /organizations/{id}
```

---

## Projects

Novo recurso:

```http
GET /projects

POST /projects

GET /projects/{id}

PUT /projects/{id}

DELETE /projects/{id}
```

---

## Assets

Mantido:

```http
/assets
```

Porém alterado o contrato.

Antes:

```json
{
"name": "Site",
"site_id": 1
}
```

Depois:

```json
{
"name": "Website Principal",
"project_id": 1,
"asset_type": "web_application",
"value": "https://empresa.com"
}
```

---

## Scans

Mantido:

```http
/scans
```

Alterações:

Antes:

```json
{
"site_id": 1
}
```

Depois:

```json
{
"project_id": 1,
"asset_id": 1
}
```

---

# Autorização Multi-Tenant

Nenhum endpoint deverá confiar somente no ID enviado pelo usuário.

Exemplo incorreto:

```python
asset = repository.get(asset_id)
```

Exemplo correto:

```python
asset = repository.get(
    asset_id,
    organization_id=current_user.organization_id
)
```

---

# Camada de Dependências

A API deverá possuir contexto autenticado:

Exemplo:

```text
Request

 ↓

JWT Token

 ↓

Current User

 ↓

Organization Context

 ↓

Resource Validation

 ↓

Controller
```

---

# Backend Impactado

## Routers

Alterar:

```text
companies.py

↓

organizations.py
```

---

```text
sites.py

↓

projects.py
```

---

Atualizar:

```text
assets.py

scans.py

signals.py

findings.py

vulnerabilities.py

recommendations.py
```

---

# Schemas Pydantic

Atualizar contratos:

Antes:

```python
CompanyCreate
SiteCreate
```

Depois:

```python
OrganizationCreate
ProjectCreate
```

---

# Repositories

Todos os repositories deverão receber contexto de Organization.

Exemplo:

Antes:

```python
find_all()
```

Depois:

```python
find_all(
    organization_id
)
```

---

# Services

Services devem garantir regras de domínio.

Exemplo:

Criar Asset:

```text
Recebe:

Asset

Project

Organization Context


Valida:

Project pertence à Organization


Cria:

Asset
```

---

# Tratamento de Erros

Padronizar respostas:

## Sem autenticação

```http
401 Unauthorized
```

---

## Sem permissão

```http
403 Forbidden
```

---

## Recurso inexistente ou fora do tenant

```http
404 Not Found
```

Não revelar existência de recursos de outros clientes.

---

# Compatibilidade

Durante a migração:

Manter:

- respostas consistentes;
- histórico;
- contratos documentados.

Caso necessário:

Criar período temporário de compatibilidade:

```text
/companies

↓

/organizations
```

com aviso de deprecated.

---

# Testes Necessários

Atualizar:

Antes:

```text
test_companies.py

test_sites.py
```

Depois:

```text
test_organizations_api.py

test_projects_api.py
```

Criar testes:

## Tenant Isolation

Usuário Organization A:

```text
GET /projects/Organization-B

Resultado:

403 ou 404
```

---

## Asset Ownership

Asset de outro Project:

```text
Negado
```

---

## Scan Authorization

Scan fora do contexto:

```text
Negado
```

---

# Critérios de Aceitação

A task será considerada concluída quando:

## API

- Endpoints refletem novo domínio;
- Organizations substitui Companies;
- Projects disponível;
- Assets usam project_id.

---

## Segurança

- Toda rota valida Organization;
- Nenhum vazamento cross-tenant;
- IDs externos não revelam dados.

---

## Arquitetura

A API representa:

```text
Organization

↓

Project

↓

Asset

↓

Scan
```

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md

002-organizations.md

003-projects.md

004-assets.md

005-multi-tenancy.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
007-data-migration.md

↓

008-frontend-refactor.md

↓

009-scan-engine-adaptation.md

↓

010-regression-tests.md
```

---

# Observação Final

A API é a fronteira pública do Mouse IA.

A arquitetura interna pode evoluir, mas os contratos HTTP precisam garantir que cada cliente visualize apenas sua própria realidade operacional.

A segurança SaaS começa no endpoint.