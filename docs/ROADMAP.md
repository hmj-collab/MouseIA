# Mouse IA Roadmap

**Versão:** 1.0  
**Status:** Planejamento Oficial

---

# Visão

O desenvolvimento do Mouse IA será orientado por versões (Releases), organizadas em Épicos e implementadas por meio de Tasks.

A arquitetura possui prioridade sobre velocidade de desenvolvimento.

Cada versão representa uma entrega funcional do produto, e não apenas um conjunto de funcionalidades técnicas.

---

# Organização

A evolução do projeto segue a seguinte estrutura:

```
Roadmap

↓

Release

↓

Epic

↓

Task

↓

Implementação
```

---

# Release v0.1 — Foundation

## Objetivo

Construir toda a fundação da plataforma.

### Epic 1 — Arquitetura

- Arquitetura oficial
- Playbook do Agent
- ADRs
- Documentação

### Epic 2 — Plataforma

- Backend
- Frontend
- Banco de Dados
- Autenticação
- Estrutura Base

### Epic 3 — Gestão

- Organizations
- Projects
- Assets

---

# Release v0.2 — Scan Platform

## Objetivo

Transformar o Mouse IA em uma plataforma de orquestração de scanners.

### Epic 1 — Scan Engine

- Engine
- Scheduler
- Workers

### Epic 2 — Providers

- HTTPX
- Nmap
- WhatWeb
- WPScan
- Nuclei
- Katana
- Naabu
- DNSX
- TestSSL
- SSLyze

### Epic 3 — Scan Management

- Execução Manual
- Execução Agendada
- Histórico
- Logs

---

# Release v0.3 — Threat Intelligence

## Objetivo

Adicionar inteligência sobre vulnerabilidades.

### Epic 1 — Correlation Engine

- Signals
- Findings
- Correlação

### Epic 2 — Vulnerability Intelligence

Integração com:

- NVD
- CISA KEV
- EPSS
- OSV
- GitHub Advisories
- WordPress.org

### Epic 3 — Risk Score

- CVSS
- EPSS
- KEV
- Peso do Asset
- Criticidade

---

# Release v0.4 — Artificial Intelligence

## Objetivo

Adicionar Inteligência Artificial.

### Epic 1 — AI Engine

- Explicações
- Resumos
- Priorização

### Epic 2 — Recommendations

- Correções
- Boas práticas
- Hardening

### Epic 3 — False Positive Analysis

- Identificação
- Sugestões
- Confiança

---

# Release v0.5 — Reporting

## Objetivo

Transformar dados em informação.

### Epic 1

Dashboard Executivo

### Epic 2

Dashboard Técnico

### Epic 3

Relatórios PDF

### Epic 4

Exportações

CSV

Excel

JSON

API

---

# Release v0.6 — Enterprise

## Objetivo

Preparar o Mouse IA para ambientes corporativos.

### Epic 1

Multiempresa

### Epic 2

RBAC

### Epic 3

Auditoria

### Epic 4

API Pública

### Epic 5

Integrações

Slack

Teams

Email

Webhook

---

# Release v1.0 — Enterprise Ready

## Objetivo

Disponibilizar a primeira versão estável.

### Critérios

- Plataforma estável
- Documentação completa
- API documentada
- Testes automatizados
- Segurança validada
- Performance validada
- Deploy automatizado

---

# Backlog Futuro

Após a versão 1.0 poderão ser incorporados novos módulos.

## Attack Surface Management

- Descoberta automática
- Inventário
- Shadow IT

## Cloud Security

- AWS
- Azure
- GCP

## Containers

- Docker
- Kubernetes

## DevSecOps

- GitHub
- GitLab
- Azure DevOps
- Bitbucket

## Mobile

- Android
- iOS

## Compliance

- LGPD
- ISO 27001
- CIS Benchmarks
- NIST CSF

## Threat Intelligence Premium

- VulnCheck
- VirusTotal
- GreyNoise
- Shodan
- Censys

---

# Modelo de Evolução

Todo desenvolvimento seguirá obrigatoriamente esta sequência.

```
Roadmap

↓

Release

↓

Epic

↓

Task

↓

Code Review

↓

Testes

↓

Documentação

↓

Release
```

Nenhuma implementação deverá ocorrer sem estar vinculada a uma Task.

Toda Task deverá pertencer a um Epic.

Todo Epic deverá pertencer a uma Release.

---

# Critérios de Evolução

Uma Release somente poderá ser considerada concluída quando:

- Todos os Épicos forem concluídos.
- Todas as Tasks forem aprovadas.
- A documentação estiver atualizada.
- Os testes estiverem aprovados.
- A arquitetura permanecer preservada.

---

# Filosofia

O Mouse IA será desenvolvido como um produto de longo prazo.

A prioridade não é entregar rapidamente.

A prioridade é construir uma plataforma sólida, escalável, modular e preparada para evoluir durante muitos anos.