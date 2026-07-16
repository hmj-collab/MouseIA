# v0.2.007 — Data Migration Strategy

## Mouse IA — Database Evolution

**Release:** v0.2  
**Task:** 007  
**Status:** Planned  
**Tipo:** Banco de Dados / Migração / Preservação Histórica

---

# Objetivo

Definir a estratégia oficial de migração dos dados existentes do Mouse IA para o novo modelo arquitetural.

Esta task garante que a evolução do domínio ocorra sem perda de dados históricos, preservando evidências de segurança, relacionamento operacional e rastreabilidade.

---

# Princípio Fundamental

A migração deve respeitar:

> Nenhuma evidência de segurança pode ser perdida durante uma alteração arquitetural.

Isso inclui:

- Organizations;
- Users;
- Projects;
- Assets;
- Scans;
- Logs;
- Signals;
- Findings;
- Vulnerabilities;
- Recommendations.

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

# Estado Atual

Banco atual:

```text
SQLite

backend/data/mouseia.db
```

Modelo atual:

```text
companies

      |

sites

      |

assets

      |

scans

      |

signals

findings

vulnerabilities

recommendations
```

---

# Estado Alvo

Modelo final:

```text
organizations

      |

projects

      |

assets

      |

scans

      |

signals

findings

vulnerabilities

recommendations
```

---

# Estratégia Geral

A migração será executada em fases controladas.

Fluxo:

```text
Backup

 ↓

Preparação

 ↓

Criação das novas estruturas

 ↓

Migração dos dados

 ↓

Validação

 ↓

Atualização da aplicação

 ↓

Remoção dos legados
```

---

# Fase 0 — Backup e Segurança

Antes de qualquer alteração:

Obrigatório:

- backup completo do banco;
- cópia do arquivo SQLite;
- registro da versão atual;
- validação dos testes existentes.

Exemplo:

```text
mouseia.db

↓

mouseia_backup_v0.1.db
```

---

# Fase 1 — Organization Migration

## Origem

Tabela:

```text
companies
```

---

## Destino

Tabela:

```text
organizations
```

---

# Estratégia

Preservar:

- id;
- name;
- description;
- timestamps.

Exemplo:

Antes:

```json
{
"id":1,
"name":"HMJ Fotografia"
}
```

Depois:

```json
{
"id":1,
"name":"HMJ Fotografia"
}
```

---

# Atualização de Relacionamentos

Antes:

```text
company_id
```

Depois:

```text
organization_id
```

Aplicar em:

- users;
- projects;
- demais entidades relacionadas.

---

# Fase 2 — Site Transformation

Esta é a etapa crítica.

A entidade Site possui responsabilidade híbrida.

Portanto:

```text
Site

↓

Project

+

Asset
```

---

# Migração Site → Project

Tabela:

Antes:

```text
sites
```

Depois:

```text
projects
```

---

Exemplo:

Entrada:

```json
{
"id":1,
"name":"HMJ Fotografia",
"url":"https://hmjfotografia.com/",
"company_id":1
}
```

Resultado:

```json
{
"id":1,
"name":"HMJ Fotografia",
"organization_id":1
}
```

---

# Migração Site → Asset

Cada Site deverá gerar automaticamente um Asset.

Exemplo:

```json
{
"project_id":1,
"name":"HMJ Fotografia Web Application",
"asset_type":"web_application",
"value":"https://hmjfotografia.com/"
}
```

---

# Preservação de IDs

Regra:

Sempre que possível:

```text
Manter IDs existentes
```

Motivo:

Preservar histórico e relacionamentos.

---

# Fase 3 — Asset Migration

Estado atual:

```text
asset.site_id
```

Estado alvo:

```text
asset.project_id
```

---

# Estratégia

Cada Asset existente deverá ser associado ao Project correspondente.

Validação:

```text
Asset

↓

Project

↓

Organization
```

---

# Fase 4 — Scan Migration

Scans possuem alto valor histórico.

Nenhum Scan deve ser recriado.

Preservar:

- id;
- data;
- status;
- resultado;
- logs.

---

# Alteração de Relacionamento

Antes:

```text
scan.site_id
```

Depois:

```text
scan.project_id
```

Manter:

```text
scan.asset_id
```

---

# Fase 5 — Signals e Findings

Signals e Findings representam evidências coletadas.

Não devem sofrer recriação.

Apenas atualizar relacionamentos.

---

# Regras:

Preservar:

- evidência original;
- severidade;
- timestamps;
- origem;
- payload técnico.

---

# Fase 6 — Vulnerabilities e Recommendations

Nenhuma vulnerabilidade deve ser perdida.

Preservar:

- CVE;
- CVSS;
- descrição;
- recomendação;
- status;
- histórico.

---

# Migration Técnica

A implementação deverá utilizar:

```text
Alembic Migration
```

---

# Requisitos

Toda migration deve possuir:

## Upgrade

Executar transformação:

```text
modelo antigo

↓

modelo novo
```

---

## Downgrade

Permitir retorno:

```text
modelo novo

↓

modelo antigo
```

---

# Estratégia SQLite

Considerando limitações do SQLite:

Utilizar:

```python
op.batch_alter_table()
```

quando necessário.

---

# Validação Pós-Migration

Após execução:

Validar:

## Quantidade de registros

Exemplo:

Antes:

```text
sites = 3
```

Depois:

```text
projects = 3
```

---

## Relacionamentos

Validar:

```text
Project possui Organization

Asset possui Project

Scan possui Asset
```

---

## Integridade

Nenhum registro órfão permitido.

---

# Rollback Strategy

Caso ocorra falha:

Executar:

```text
Parar aplicação

↓

Restaurar backup

↓

Executar diagnóstico

↓

Corrigir migration

↓

Executar novamente
```

---

# Testes Necessários

Criar validações:

## Migration Test

Executar migration em banco temporário.

---

## Data Integrity Test

Comparar:

Antes:

```text
Quantidade de registros
```

Depois:

```text
Quantidade de registros
```

---

## Security Test

Garantir:

```text
Organization A

não acessa

Organization B
```

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Dados

- Nenhum dado perdido;
- Histórico preservado;
- Relacionamentos corretos.

---

## Banco

- Nova estrutura criada;
- Migração executada;
- Rollback validado.

---

## Segurança

- Isolamento multi-tenant preservado.

---

# Dependências

Pré-requisitos:

```text
001-domain-migration.md

002-organizations.md

003-projects.md

004-assets.md

005-multi-tenancy.md

006-api-refactor.md
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
008-frontend-refactor.md

↓

009-scan-engine-adaptation.md

↓

010-regression-tests.md
```

---

# Observação Final

A migração de dados é o ponto onde a arquitetura planejada encontra o sistema real.

O sucesso desta etapa será medido não apenas pela aplicação funcionar, mas pela garantia de que todo histórico de segurança acumulado pelo Mouse IA continue válido após sua evolução para uma plataforma SaaS.