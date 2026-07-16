# v0.2.009 — Scan Engine Adaptation

## Mouse IA — Asset Based Security Engine

**Release:** v0.2  
**Task:** 009  
**Status:** Planned  
**Tipo:** Backend / Security Engine / Architecture

---

# Objetivo

Adaptar o Scan Engine do Mouse IA para operar baseado em Assets, removendo o acoplamento existente com a entidade Site.

Esta task transforma o motor de varredura de um mecanismo orientado a websites para uma arquitetura extensível baseada em recursos monitorados.

---

# Princípio Fundamental

O Scan Engine deve conhecer:

```text
O que analisar

e não

como o recurso foi cadastrado.
```

O motor deve receber um Asset e decidir qual estratégia de análise aplicar.

---

# Documentos de Referência

Esta task deve respeitar:

- ARCHITECTURE.md
- AGENT.md
- DOMAIN.md
- SECURITY.md
- DECISIONS.md
- PLANO_DE_MIGRAÇÃO_ARQUITETURAL.md

Relacionada diretamente:

- 003-projects.md
- 004-assets.md
- 007-data-migration.md
- 008-frontend-refactor.md

---

# Contexto Atual

O Scan Engine atual utiliza a entidade Site como origem do alvo.

Fluxo atual:

```text
Scan

 ↓

Site

 ↓

URL

 ↓

Scanner
```

Exemplo:

```python
site.url

↓

https://empresa.com
```

---

# Problema Identificado

O modelo atual limita a evolução do produto.

O scanner assume que todo recurso monitorado é um website.

Consequências:

- dificuldade para adicionar novos scanners;
- lógica acoplada ao domínio Site;
- baixa reutilização;
- impossibilidade de ASM real.

---

# Decisão Arquitetural

O Scan Engine deverá ser orientado por Asset.

Novo fluxo:

```text
Scan

 ↓

Asset

 ↓

Asset Type

 ↓

Scanner Handler

 ↓

Findings
```

---

# Novo Modelo de Execução

Exemplo:

Asset:

```json
{
"type":"web_application",
"value":"https://empresa.com"
}
```

Processamento:

```text
Asset

↓

WebApplicationScanner

↓

HTTP Tests

↓

DNS Tests

↓

Security Headers

↓

WordPress Detection

↓

Findings
```

---

# Arquitetura de Scanners

Criar conceito:

```text
Scanner Interface
```

---

Exemplo conceitual:

```python
class Scanner:

    def execute(asset):
        pass
```

---

Implementações:

```text
WebApplicationScanner

DNSScanner

RepositoryScanner

CloudScanner
```

---

# Asset Type Routing

O Scan Engine deverá decidir o scanner baseado em:

```text
asset_type
```

Exemplo:

```text
web_application

↓

WebApplicationScanner
```

---

```text
domain

↓

DNSScanner
```

---

```text
repository

↓

RepositoryScanner
```

---

# Migração do Scanner Atual

O scanner existente deverá ser preservado.

A lógica atual:

- DNS;
- headers HTTP;
- WordPress;
- arquivos expostos;
- rotas sensíveis;

deve ser movida para:

```text
WebApplicationScanner
```

---

# Alteração do Scan Service

Antes:

```text
ScanService

recebe:

Site
```

Depois:

```text
ScanService

recebe:

Asset
```

---

# Novo Fluxo

```text
Usuário inicia Scan

        ↓

Seleciona Project

        ↓

Seleciona Asset

        ↓

Cria Scan

        ↓

Engine identifica Asset Type

        ↓

Seleciona Scanner

        ↓

Executa análise

        ↓

Gera Findings
```

---

# Relacionamento Scan

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

# Logs

Os logs de execução devem continuar preservados.

Manter:

- início;
- progresso;
- mensagens;
- erros;
- conclusão.

---

# Background Processing

O desenho atual permite evolução futura.

Estado atual:

```text
FastAPI Background Task
```

Estado futuro:

```text
Celery Worker

        +

Redis Queue
```

---

# Segurança

O Scan Engine deve validar:

```text
Usuário

↓

Organization

↓

Project

↓

Asset

↓

Scan
```

Nenhum scan pode ser executado em Asset fora do tenant.

---

# Correlação de Vulnerabilidades

O CorrelationService deverá continuar funcionando.

Alteração:

Antes:

```text
Finding

↓

Site Context
```

Depois:

```text
Finding

↓

Asset Context

↓

Project Context
```

---

# Estrutura Esperada

Novo conceito:

```text
scan_engine/

├── base.py

├── web_application.py

├── dns.py

├── repository.py

└── cloud.py
```

---

# Estratégia de Implementação

Executar:

```text
1. Criar interface Scanner

        ↓

2. Migrar scanner atual para WebApplicationScanner

        ↓

3. Alterar ScanService

        ↓

4. Implementar Asset Routing

        ↓

5. Validar Findings

        ↓

6. Remover dependência Site
```

---

# Testes Necessários

Criar testes:

## Web Application Asset

Entrada:

```text
asset_type = web_application
```

Resultado:

```text
WebApplicationScanner executado
```

---

## Domain Asset

Entrada:

```text
asset_type = domain
```

Resultado:

```text
DNSScanner executado
```

---

## Tenant Validation

Asset de outra Organization:

Resultado:

```text
Scan bloqueado
```

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Arquitetura

- Scan Engine não depender de Site;
- Asset for entrada principal;
- Scanner baseado em tipo de ativo.

---

## Segurança

- Scan respeitar isolamento multi-tenant;
- Asset sempre validado.

---

## Evolução

Novo scanner pode ser adicionado sem alterar o núcleo do Scan Engine.

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

007-data-migration.md

008-frontend-refactor.md
```

---

# Próxima Task

Após conclusão:

```text
010-regression-tests.md
```

---

# Observação Final

A adaptação do Scan Engine é o ponto onde o Mouse IA deixa de ser uma aplicação focada em websites e passa a possuir arquitetura compatível com uma plataforma moderna de Attack Surface Management.

O ativo é o centro da análise.

O scanner é apenas uma capacidade especializada.