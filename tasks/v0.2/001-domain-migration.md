# v0.2.001 — Domain Migration Foundation

## Mouse IA — Architecture Alignment

**Release:** v0.2  
**Task:** 001  
**Status:** Planned  
**Tipo:** Arquitetura / Migração de Domínio

---

# Objetivo

Realizar o alinhamento do modelo de domínio implementado atualmente no Mouse IA com a arquitetura oficial definida nos documentos de referência do projeto.

Esta task representa o início da Release v0.2 e estabelece a fundação para todas as alterações posteriores de backend, frontend, banco de dados e processamento.

O objetivo principal é eliminar divergências entre:

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

e o modelo oficial:

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

# Documentos de Referência

Esta task deve respeitar obrigatoriamente:

- ARCHITECTURE.md
- AGENT.md
- DOMAIN.md
- DECISIONS.md
- ROADMAP.md
- SECURITY.md
- PLANO_DE_MIGRAÇÃO_ARQUITETURAL.md

Em caso de conflito, aplicar a regra definida na ADR-010:

> Documentação oficial é a fonte de verdade da aplicação.

---

# Contexto Atual

A análise realizada no sistema identificou que o modelo atual possui divergências arquiteturais.

## Entidades atuais

```text
Company

Responsável por representar empresas/clientes.


Site

Responsabilidade híbrida:

- Container operacional;
- Recurso técnico monitorado.


Asset

Recurso técnico vinculado diretamente ao Site.


Scan

Executado considerando o Site como alvo.
```

---

# Problema Identificado

A entidade Site viola o princípio de responsabilidade única.

Ela representa simultaneamente:

## Container operacional

Exemplo:

```text
Projeto de segurança da HMJ Fotografia
```

## Recurso monitorado

Exemplo:

```text
https://hmjfotografia.com/
```

Essa combinação limita a evolução do produto para:

- múltiplos ativos por projeto;
- Attack Surface Management;
- ambientes Enterprise;
- segregação multi-tenant;
- novos tipos de ativos.

---

# Decisão Arquitetural

Conforme definido na ADR-014:

A entidade Site deixa de existir como entidade de domínio.

Cada Site legado será transformado em:

```text
Site legado

        ↓

Project
+
Asset
```

---

# Modelo de Domínio Alvo

A arquitetura oficial será:

```text
Organization

    |
    |

Project

    |
    |

Asset

    |
    |

Scan

    |
    |

Signal

    |
    |

Finding

    |
    |

Vulnerability

    |
    |

Recommendation

    |
    |

Task
```

---

# Escopo

Esta task contempla somente o planejamento e preparação da migração.

Inclui:

## Domínio

- Definição do modelo Organization;
- Definição do modelo Project;
- Definição do relacionamento Asset → Project;
- Remoção conceitual da entidade Site.

---

## Banco de Dados

Preparar estratégia para:

- companies → organizations;
- sites → projects;
- criação automática de assets derivados dos sites;
- atualização dos relacionamentos existentes;
- preservação dos IDs históricos.

---

## Compatibilidade

Garantir que a migração preserve:

- usuários;
- permissões;
- organizações;
- projetos;
- ativos;
- scans;
- signals;
- findings;
- vulnerabilidades;
- recomendações.

---

# Fora do Escopo

Esta task NÃO contempla:

- Implementação de migrations Alembic;
- Alteração dos modelos SQLAlchemy;
- Alteração das APIs;
- Alteração do frontend;
- Migração real de dados;
- Mudança para PostgreSQL;
- Implementação Redis/Celery;
- Novos scanners.

Esses itens serão tratados em tasks específicas da Release v0.2.

---

# Dependências

Esta task depende de:

```text
ADR-010
Documentação como Fonte de Verdade

ADR-014
Separação de Containers Operacionais e Recursos Monitorados

PLANO_DE_MIGRAÇÃO_ARQUITETURAL
```

---

# Estratégia de Execução

A migração deverá seguir uma abordagem incremental.

Fluxo:

```text
1. Validar domínio

        ↓

2. Criar novas estruturas

        ↓

3. Migrar dados

        ↓

4. Validar integridade

        ↓

5. Alterar consumidores

        ↓

6. Remover estruturas antigas
```

---

# Fases Planejadas

## Fase 1 — Preparação

Objetivo:

Garantir entendimento completo do impacto.

Validações:

- modelos atuais;
- relacionamentos;
- testes existentes;
- dados persistidos.

---

## Fase 2 — Organização

Transformação:

```text
Company

↓

Organization
```

Preservar:

- IDs;
- usuários;
- permissões;
- histórico.

---

## Fase 3 — Projeto

Transformação:

```text
Site

↓

Project
```

Preservar:

- identificação;
- descrição;
- vínculo organizacional.

---

## Fase 4 — Assets

Transformação:

```text
Site.url

↓

Asset.value
```

Criando:

```json
{
 "asset_type": "web_application",
 "value": "URL_original",
 "project_id": "novo_project"
}
```

---

## Fase 5 — Relacionamentos

Atualizar:

Antes:

```text
Asset
 |
 site_id
```

Depois:

```text
Asset
 |
 project_id
```

Antes:

```text
Scan
 |
 site_id
```

Depois:

```text
Scan
 |
 project_id
 |
 asset_id
```

---

# Estratégia de Segurança

Durante toda migração:

- Nenhum dado deve ser perdido;
- Nenhum tenant deve acessar dados de outro tenant;
- Nenhuma evidência de segurança deve ser removida;
- Histórico deve permanecer auditável.

---

# Estratégia de Rollback

Toda alteração deverá possuir possibilidade de reversão.

Obrigatório:

- Backup anterior à migração;
- Registro das alterações executadas;
- Validação após cada etapa;
- Possibilidade de retorno ao estado anterior.

A migração não deverá remover estruturas antigas antes da validação completa.

---

# Critérios de Aceitação

Esta task será considerada concluída quando:

## Documentação

- Modelo antigo documentado;
- Modelo novo documentado;
- Estratégia de migração aprovada.

---

## Arquitetura

- Organization definido como tenant raiz;
- Project definido como container operacional;
- Asset definido como recurso monitorado;
- Site removido conceitualmente.

---

## Segurança

- Estratégia multi-tenant definida;
- Histórico preservado;
- Rollback definido.

---

## Preparação

Todas as próximas tasks da Release v0.2 conseguem utilizar este documento como referência.

---

# Próximas Tasks Dependentes

Após conclusão:

```text
002-organizations.md

↓

003-projects.md

↓

004-assets.md

↓

005-multi-tenancy.md

↓

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

A Release v0.2 não representa criação de novas funcionalidades.

Ela representa a correção estrutural do domínio do Mouse IA para permitir evolução segura como plataforma de segurança multi-tenant.

A qualidade desta migração define a capacidade futura de expansão do produto.