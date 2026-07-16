# v0.2.002 — Organizations Domain Migration

## Mouse IA — Architecture Alignment

**Release:** v0.2  
**Task:** 002  
**Status:** Planned  
**Tipo:** Arquitetura / Migração de Domínio

---

# Objetivo

Migrar a entidade atual `Company` para a entidade oficial `Organization`, alinhando a implementação existente com o modelo de domínio definido pelo Mouse IA.

Esta task representa a primeira alteração estrutural do domínio da Release v0.2, pois `Organization` é a entidade raiz responsável pelo isolamento multi-tenant da plataforma.

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

---

# Contexto Atual

A implementação atual utiliza o conceito:

```text
Company
```

como entidade raiz do cliente.

Estrutura atual:

```text
Company

   |
   |

Site

   |
   |

Asset

   |
   |

Scan
```

---

# Problema Identificado

O termo `Company` representa uma limitação conceitual.

O Mouse IA não é apenas uma ferramenta interna de uma empresa.

A plataforma deve suportar:

- múltiplos clientes;
- ambientes isolados;
- organizações Enterprise;
- futuros modelos SaaS;
- diferentes unidades operacionais.

O conceito correto de domínio é:

```text
Organization
```

---

# Decisão Arquitetural

A entidade:

```text
Company
```

será substituída conceitualmente por:

```text
Organization
```

A Organization será o Tenant Root da aplicação.

Modelo oficial:

```text
Organization

      |
      |

Project

      |
      |

Asset
```

---

# Responsabilidade da Organization

A Organization representa:

- cliente da plataforma;
- limite de isolamento de dados;
- contexto de autorização;
- agrupador superior de Projects;
- unidade de auditoria.

---

# Escopo

Esta task contempla:

## Backend

Alterações previstas:

Model:

```text
company.py

↓

organization.py
```

Classe:

```python
Company

↓

Organization
```

---

Schemas:

```text
company.py

↓

organization.py
```

Alterações esperadas:

```text
CompanyCreate

↓

OrganizationCreate


CompanyOut

↓

OrganizationOut


CompanyUpdate

↓

OrganizationUpdate
```

---

Repositories:

```text
company_repository.py

↓

organization_repository.py
```

---

Services:

```text
company_service.py

↓

organization_service.py
```

---

API:

Antes:

```http
/companies
```

Depois:

```http
/organizations
```

---

# Banco de Dados

Estado atual:

```text
companies
```

Estado alvo:

```text
organizations
```

---

## Estratégia de Migração

A migração deverá preservar:

- IDs existentes;
- timestamps;
- relacionamentos;
- histórico operacional.

Exemplo:

Antes:

```text
companies

id = 1
name = Cliente A
```

Depois:

```text
organizations

id = 1
name = Cliente A
```

---

# Relacionamentos

Antes:

```text
User

 |
 company_id
```

Depois:

```text
User

 |
 organization_id
```

---

Antes:

```text
Site

 |
 company_id
```

Depois:

```text
Project

 |
 organization_id
```

---

# Segurança Multi-Tenant

Organization passa a ser a fronteira obrigatória de autorização.

Toda operação deverá validar:

```text
Usuário autenticado

        |

Organization permitida

        |

Recurso solicitado
```

Nenhum endpoint poderá confiar somente em IDs enviados pelo cliente.

---

# Compatibilidade

Durante a migração:

Garantir:

- preservação dos usuários;
- preservação das permissões;
- preservação dos registros históricos;
- preservação dos relacionamentos existentes.

---

# Fora do Escopo

Esta task NÃO contempla:

- criação de Projects;
- transformação de Sites;
- criação de Assets derivados;
- alteração do Scan Engine;
- mudança para PostgreSQL;
- implementação Redis/Celery.

Esses itens pertencem às próximas tasks.

---

# Estratégia de Implementação

A alteração deverá ocorrer em etapas:

```text
1. Criar modelo Organization

        ↓

2. Criar migration de banco

        ↓

3. Migrar dados Company

        ↓

4. Atualizar backend

        ↓

5. Atualizar testes

        ↓

6. Validar isolamento
```

---

# Testes Necessários

Atualizar:

Antes:

```text
test_companies.py
```

Depois:

```text
test_organizations.py
```

Validar:

- criação;
- consulta;
- atualização;
- autorização;
- isolamento.

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Domínio

- Não existir mais referência conceitual a Company;
- Organization for a entidade raiz oficial.

---

## Backend

- Model Organization implementado;
- Schemas atualizados;
- Services atualizados;
- Repositories atualizados;
- Rotas atualizadas.

---

## Banco

- Migration criada;
- Dados preservados;
- Relacionamentos atualizados.

---

## Segurança

- Organization definida como boundary de autorização;
- Nenhum acesso cross-tenant permitido.

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
003-projects.md

↓

004-assets.md

↓

005-multi-tenancy.md
```

---

# Observação Final

A migração de Company para Organization não é apenas uma mudança de nomenclatura.

Ela representa a consolidação do Mouse IA como plataforma multi-tenant, onde cada Organization possui controle isolado sobre seus Projects, Assets e dados operacionais.