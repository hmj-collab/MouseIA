# v0.2.005 — Multi-Tenancy Architecture

## Mouse IA — SaaS Foundation

**Release:** v0.2  
**Task:** 005  
**Status:** Planned  
**Tipo:** Arquitetura / Segurança / SaaS

---

# Objetivo

Implementar a fundação arquitetural necessária para transformar o Mouse IA em uma plataforma SaaS multi-tenant.

Esta task define as regras de isolamento, autorização e governança dos dados entre diferentes organizações utilizando a arquitetura:

```text
Organization

      |

   Project

      |

    Asset

      |

    Scan

      |

 Finding / Vulnerability
```

---

# Visão SaaS

O Mouse IA deverá suportar múltiplos clientes utilizando a mesma plataforma.

Exemplo:

```text
Mouse IA SaaS

        |

        +----------------+
        |                |
        ↓                ↓

Organization A     Organization B

Cliente A          Cliente B

        |                |

 Projects           Projects

 Assets             Assets

 Scans              Scans
```

Cada Organization deve operar como um ambiente logicamente isolado.

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

# Problema Atual

A implementação atual possui isolamento parcial.

Existem referências:

```text
company_id
site_id
```

Porém não existe uma garantia arquitetural centralizada de tenant isolation.

---

# Risco Atual

Sem validação consistente:

Um usuário autenticado poderia potencialmente:

```text
Consultar:

/assets/123


Mesmo sem pertencer à Organization dona do Asset.
```

Isso representa risco crítico:

```text
Cross Tenant Data Exposure
```

---

# Decisão Arquitetural

Organization será a fronteira máxima de isolamento.

Toda entidade operacional deverá possuir caminho de validação até sua Organization.

Modelo:

```text
User

 |

Organization

 |

Project

 |

Asset

 |

Scan

 |

Finding

 |

Vulnerability
```

---

# Regras de Isolamento

## Regra 1 — Usuário pertence a uma Organization

Todo usuário deverá possuir:

```text
organization_id
```

---

## Regra 2 — Project pertence a uma Organization

Obrigatório:

```text
Project.organization_id
```

---

## Regra 3 — Asset pertence a Project

Obrigatório:

```text
Asset.project_id
```

A validação deverá alcançar:

```text
Asset

↓

Project

↓

Organization
```

---

## Regra 4 — Scan pertence ao contexto correto

Um Scan deverá respeitar:

```text
Scan

↓

Project

↓

Organization
```

e:

```text
Scan

↓

Asset
```

---

# Modelo de Autorização

Fluxo obrigatório:

```text
Request

   |

Usuário autenticado

   |

Organization do usuário

   |

Recurso solicitado

   |

Validação

   |

Permitir / Negar
```

---

# Backend

## Dependência de Tenant

Criar mecanismo centralizado:

Exemplo conceitual:

```python
get_current_user()

        +

validate_organization_access()
```

Toda rota protegida deverá utilizar essa validação.

---

# Repositories

Repositories não devem confiar apenas em IDs.

Evitar:

```python
get_asset(asset_id)
```

Preferir:

```python
get_asset(
 asset_id,
 organization_id
)
```

---

# Services

Services devem receber contexto:

Antes:

```python
create_asset(asset)
```

Depois:

```python
create_asset(
 asset,
 organization_context
)
```

---

# RBAC

A arquitetura deverá permitir evolução para:

```text
Organization Owner

Administrator

Security Analyst

Viewer

Auditor
```

---

# Permissões Esperadas

## Owner

Pode:

- gerenciar usuários;
- gerenciar projetos;
- visualizar tudo da Organization.

---

## Administrator

Pode:

- gerenciar ativos;
- executar scans;
- administrar configurações.

---

## Security Analyst

Pode:

- analisar findings;
- tratar vulnerabilidades;
- criar recomendações.

---

## Viewer

Pode:

- visualizar dados autorizados.

---

# Auditoria

Toda ação sensível deverá permitir rastreamento futuro:

Exemplos:

```text
Usuário X

criou Asset Y

na Organization Z

em horário T
```

Eventos futuros:

- login;
- criação;
- alteração;
- exclusão;
- execução de scan;
- alteração de vulnerabilidade.

---

# Banco de Dados

Todos os registros sensíveis devem possuir caminho determinístico para Organization.

Modelo:

```text
organizations

id


projects

id
organization_id


assets

id
project_id


scans

id
project_id
asset_id


findings

id
asset_id


vulnerabilities

id
finding_id
```

---

# Estratégia de Consulta Segura

Todas as consultas devem aplicar filtro de tenant.

Exemplo:

Errado:

```sql
SELECT *
FROM assets
WHERE id = 10;
```

Correto:

```sql
SELECT *
FROM assets
WHERE id = 10
AND project_id IN (
    SELECT id
    FROM projects
    WHERE organization_id = :organization_id
);
```

---

# Preparação para SaaS Enterprise

Esta arquitetura permitirá futuramente:

## Planos

Exemplo:

```text
Free

Professional

Enterprise
```

---

## Limites por Organization

Exemplo:

```text
Quantidade de:

- usuários;
- projetos;
- ativos;
- scans;
```

---

## Billing

Possível integração:

- Stripe;
- gateways nacionais;
- contratos Enterprise.

---

## Isolamento Futuro

A arquitetura permite evolução para:

```text
Shared Database

        ↓

Schema per Tenant

        ↓

Database per Tenant
```

---

# Fora do Escopo

Esta task NÃO implementa:

- Billing;
- Planos;
- Pagamentos;
- Marketplace;
- SSO;
- MFA;
- Kubernetes;
- Banco separado por cliente.

---

# Estratégia de Implementação

Ordem:

```text
1. Definir Organization como tenant root

        ↓

2. Criar validações centrais

        ↓

3. Ajustar repositories

        ↓

4. Ajustar services

        ↓

5. Validar endpoints

        ↓

6. Criar testes de isolamento
```

---

# Testes Obrigatórios

Criar cenários:

## Cenário 1

Usuário A acessa dados da Organization A.

Resultado:

```text
Permitido
```

---

## Cenário 2

Usuário A tenta acessar dados da Organization B.

Resultado:

```text
Negado
```

---

## Cenário 3

Asset pertence ao Project correto.

Resultado:

```text
Permitido
```

---

## Cenário 4

Scan tenta executar em Asset externo.

Resultado:

```text
Negado
```

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Segurança

- Nenhum cross-tenant access permitido;
- Organization é boundary oficial;
- Validação centralizada criada.

---

## Arquitetura

- Todos recursos possuem caminho até Organization;
- Repositories respeitam tenant;
- Services recebem contexto.

---

## SaaS

A plataforma suporta:

- múltiplas Organizations;
- usuários isolados;
- dados segregados.

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md

002-organizations.md

003-projects.md

004-assets.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
006-api-refactor.md

↓

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

A implementação de Multi-Tenancy é a transição do Mouse IA de uma aplicação funcional para uma plataforma SaaS.

A segurança do produto dependerá diretamente da correta aplicação dessas regras.

A premissa fundamental:

"Um cliente do Mouse IA nunca deve saber que outro cliente existe."