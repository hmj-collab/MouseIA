# v0.2.010 — Regression Tests

## Mouse IA — Architecture Migration Validation

**Release:** v0.2  
**Task:** 010  
**Status:** Planned  
**Tipo:** Quality Assurance / Validation / Release Gate

---

# Objetivo

Validar que todas as alterações realizadas durante a evolução arquitetural da versão v0.2 foram implementadas corretamente sem regressão funcional, perda de dados ou falhas de isolamento.

Esta task representa o critério final para considerar a migração arquitetural concluída.

---

# Princípio Fundamental

A conclusão da v0.2 exige comprovação de que:

> O Mouse IA evoluiu de uma aplicação funcional para uma plataforma SaaS segura, mantendo todos os recursos existentes.

---

# Documentos de Referência

Esta validação deve respeitar:

- ARCHITECTURE.md
- AGENT.md
- DOMAIN.md
- SECURITY.md
- DECISIONS.md
- PLANO_DE_MIGRAÇÃO_ARQUITETURAL.md

Tasks relacionadas:

```text
001-domain-migration.md

002-organizations.md

003-projects.md

004-assets.md

005-multi-tenancy.md

006-api-refactor.md

007-data-migration.md

008-frontend-refactor.md

009-scan-engine-adaptation.md
```

---

# Escopo de Validação

A regressão será dividida em:

```text
1. Banco de Dados

2. Backend API

3. Segurança Multi-Tenant

4. Scan Engine

5. Frontend

6. Dados Históricos

7. Performance
```

---

# 1. Database Validation

## Objetivo

Garantir que a nova estrutura de dados está íntegra.

---

## Validar entidades principais

Esperado:

```text
organizations

projects

assets

scans

signals

findings

vulnerabilities

recommendations
```

---

## Validar relacionamentos

Obrigatório:

```text
Organization

↓

Project

↓

Asset

↓

Scan

↓

Finding

↓

Vulnerability
```

---

## Validar ausência de órfãos

Nenhum registro deve existir sem contexto.

Exemplos:

Asset sem Project:

```text
Falha
```

Scan sem Asset:

```text
Falha
```

---

# 2. Backend API Validation

## Authentication

Validar:

```text
/login

/me
```

Resultado esperado:

Usuário autenticado recebe contexto correto.

---

# Organizations API

Validar:

```http
GET /organizations

POST /organizations

PUT /organizations/{id}

DELETE /organizations/{id}
```

---

# Projects API

Validar:

```http
GET /projects

POST /projects

PUT /projects/{id}

DELETE /projects/{id}
```

---

# Assets API

Validar:

```http
GET /assets

POST /assets
```

Com:

```json
{
"project_id":1
}
```

---

# Scans API

Validar:

```http
POST /scans

POST /scans/{id}/launch
```

Com:

```json
{
"project_id":1,
"asset_id":1
}
```

---

# 3. Multi-Tenant Security Validation

## Objetivo

Garantir a principal regra SaaS:

> Um cliente do Mouse IA nunca deve saber que outro cliente existe.

---

# Teste Organization Isolation

Criar:

```text
Organization A

Organization B
```

Usuário:

```text
User A pertence à Organization A
```

---

Tentativa:

```text
User A acessar Project da Organization B
```

Resultado esperado:

```http
403 Forbidden

ou

404 Not Found
```

---

# Teste Asset Isolation

Cenário:

```text
Asset B pertence à Organization B
```

Usuário A tenta:

```http
GET /assets/B
```

Resultado:

```text
Bloqueado
```

---

# Teste Scan Isolation

Usuário A tenta executar:

```text
Scan em Asset externo
```

Resultado:

```text
Negado
```

---

# 4. Scan Engine Validation

## Objetivo

Confirmar que o motor agora opera baseado em Assets.

---

# Web Application Scanner

Entrada:

```json
{
"asset_type":"web_application"
}
```

Esperado:

```text
WebApplicationScanner executado
```

---

# Domain Scanner

Entrada:

```json
{
"asset_type":"domain"
}
```

Esperado:

```text
DNSScanner executado
```

---

# Finding Generation

Validar:

```text
Scan

↓

Finding

↓

Vulnerability
```

---

# 5. Historical Data Validation

## Objetivo

Garantir preservação do histórico.

---

Validar:

Antes da migração:

```text
Quantidade de scans
Quantidade de findings
Quantidade de vulnerabilities
```

Depois:

```text
Mesmo volume preservado
```

---

# Dados Críticos

Nenhuma perda permitida:

- CVEs;
- CVSS;
- evidências;
- logs;
- timestamps;
- recomendações.

---

# 6. Frontend Validation

## Navegação

Esperado:

```text
Dashboard

Organizações

Projetos

Ativos

Scans

Ameaças

Vulnerabilidades
```

---

# Fluxos Principais

## Criar Organization

Resultado:

```text
Organization criada
```

---

## Criar Project

Resultado:

```text
Project associado corretamente
```

---

## Criar Asset

Resultado:

```text
Asset aparece dentro do Project
```

---

## Executar Scan

Resultado:

```text
Logs exibidos

Findings gerados
```

---

# 7. Automated Tests

Todos os testes existentes devem continuar funcionando.

Meta:

```text
100% sucesso
```

---

# Cobertura Esperada

Backend:

```text
Authentication

Organizations

Projects

Assets

Scans

Correlation

Vulnerabilities
```

---

Frontend:

```text
Login

Dashboard

CRUD

Scan Flow

Threat Visualization
```

---

# Performance Validation

Validar comportamento básico:

## Concorrência

Executar múltiplos scans.

Esperado:

```text
Sistema permanece responsivo
```

---

## Banco

Validar:

- consultas;
- relacionamentos;
- filtros por tenant.

---

# SaaS Readiness Checklist

A versão v0.2 será considerada aprovada quando:

---

## Domínio

✅ Organization como tenant root

✅ Project como container operacional

✅ Asset como recurso monitorado

---

## Segurança

✅ Isolamento multi-tenant

✅ RBAC funcionando

✅ Sem vazamento entre clientes

---

## Dados

✅ Migração concluída

✅ Histórico preservado

---

## API

✅ Contratos atualizados

✅ Endpoints alinhados ao domínio

---

## Frontend

✅ Interface SaaS

✅ Novo modelo representado

---

## Engine

✅ Scan baseado em Asset

✅ Scanner extensível

---

# Critério Final de Aprovação

A v0.2 está concluída quando:

```text
Um novo cliente consegue utilizar o Mouse IA

sem conhecer a existência de outros clientes,

com seus dados isolados,

seus ativos organizados,

suas análises executadas,

e seu histórico preservado.
```

---

# Resultado Esperado

Ao concluir esta task:

O Mouse IA estará oficialmente migrado para sua arquitetura SaaS inicial.

Próxima evolução:

```text
v0.3

Enterprise Security Platform Features
```

---

# Observação Final

A v0.2 não representa apenas uma refatoração técnica.

Ela representa a mudança de categoria do produto:

De:

```text
Ferramenta de Scanner
```

Para:

```text
Plataforma SaaS de Gestão de Superfície de Ataque
```