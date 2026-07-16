# Mouse IA Architecture

**Versão:** 1.0  
**Status:** Draft  
**Última atualização:** Julho/2026

---

# 1. Visão

O Mouse IA é uma plataforma profissional de Attack Surface Management (ASM), Vulnerability Management (VM) e Threat Intelligence desenvolvida para automatizar a descoberta, análise, correlação e gestão de vulnerabilidades em ativos digitais.

O objetivo da plataforma não é substituir ferramentas especializadas como Nmap, Nuclei, WPScan ou WhatWeb.

Essas ferramentas serão utilizadas como Providers.

O diferencial do Mouse IA será a orquestração dessas ferramentas, a normalização das evidências coletadas, a correlação inteligente das informações e a geração de recomendações utilizando Inteligência Artificial.

---

# 2. Objetivos

A plataforma deverá permitir:

- Gestão centralizada de Assets
- Execução automatizada de Scans
- Coleta de Signals
- Correlação automática
- Identificação de Vulnerabilidades
- Priorização baseada em risco
- Gestão de Recomendações
- Gestão de Tasks
- Dashboards Executivos
- Relatórios Técnicos
- Multiempresa
- API Pública

---

# 3. Princípios Arquiteturais

Toda decisão arquitetural deverá respeitar os seguintes princípios.

## Clean Architecture

Separação clara entre domínio, aplicação e infraestrutura.

## SOLID

Todo componente deverá possuir responsabilidade única.

## Security First

Toda funcionalidade deve priorizar segurança.

## Fail Fast

Falhas devem ser detectadas rapidamente.

## Observabilidade

Todo processamento deve gerar logs e métricas.

## Escalabilidade

O crescimento da plataforma nunca deverá exigir reescrita da arquitetura.

---

# 4. Arquitetura Geral

```
Frontend

↓

API Gateway

↓

Application Layer

↓

Domain Layer

↓

Infrastructure Layer

↓

Providers

↓

Threat Intelligence

↓

Artificial Intelligence
```

Cada camada possui responsabilidade única.

---

# 5. Componentes da Plataforma

A plataforma será composta pelos seguintes módulos.

## Dashboard

Responsável pela experiência do usuário.

## Authentication

Autenticação.

Autorização.

RBAC.

MFA futuramente.

## Organizations

Empresas.

## Projects

Projetos.

## Assets

Recursos monitorados.

## Scheduler

Agendamento de execuções.

## Scan Engine

Motor responsável pela orquestração dos scanners.

## Providers

Integrações com ferramentas externas.

## Correlation Engine

Responsável pela interpretação dos Signals.

## Threat Intelligence

Responsável pelo enriquecimento das informações.

## AI Engine

Responsável pela análise inteligente.

## Reporting

Relatórios.

---

# 6. Fluxo Oficial

```
Organization

↓

Project

↓

Asset

↓

Scan

↓

Providers

↓

Signals

↓

Correlation Engine

↓

Findings

↓

Threat Intelligence

↓

Vulnerabilities

↓

AI Engine

↓

Recommendations

↓

Tasks

↓

Reports
```

Este fluxo deverá ser seguido por toda a plataforma.

---

# 7. Modelo Conceitual

## Organization

Empresa.

## Project

Agrupamento lógico.

## Asset

Qualquer recurso monitorado.

Exemplos:

- Website
- WordPress
- API
- Linux
- Windows
- Docker
- Kubernetes
- GitHub
- Azure DevOps
- GitLab
- Cloudflare

---

## Scan

Execução completa de auditoria.

---

## Signal

Informação coletada.

Nunca representa vulnerabilidade.

Exemplos:

- Header HTTP
- Porta aberta
- Plugin detectado
- PHP 8.3
- TLS 1.3
- DNS
- Banner

---

## Finding

Interpretação de um ou mais Signals.

---

## Vulnerability

Vulnerabilidade validada.

Pode possuir:

- CVE
- EPSS
- KEV
- CVSS
- Exploit Público
- Patch

---

## Recommendation

Correção recomendada.

---

## Task

Atividade criada para acompanhamento.

---

# 8. Providers

O Mouse IA utilizará ferramentas especializadas.

Exemplos:

- Nmap
- Nuclei
- WhatWeb
- WPScan
- Katana
- Httpx
- Naabu
- DNSX
- Subfinder
- TestSSL
- SSLyze
- Nikto
- CMSeeK

Cada Provider deverá possuir interface própria.

Providers nunca conterão regra de negócio.

---

# 9. Threat Intelligence

A camada de inteligência será responsável por enriquecer os Findings.

Fontes previstas:

- NVD
- CISA KEV
- EPSS
- OSV
- GitHub Advisories
- WordPress.org
- VulnCheck
- OTX

Nenhum scanner consultará diretamente essas bases.

Toda consulta ocorrerá exclusivamente através da camada Threat Intelligence.

---

# 10. Artificial Intelligence

A Inteligência Artificial nunca executará scanners.

A IA receberá:

- Signals
- Findings
- Vulnerabilities

A IA poderá:

- Priorizar riscos
- Explicar vulnerabilidades
- Identificar falsos positivos
- Gerar recomendações
- Resumir relatórios
- Auxiliar decisões

Toda resposta deverá informar nível de confiança.

---

# 11. Segurança

A plataforma deverá utilizar:

- JWT
- RBAC
- Auditoria
- Logs
- HTTPS
- Criptografia de credenciais
- Princípio do menor privilégio

---

# 12. Observabilidade

Todos os componentes deverão produzir:

- Logs estruturados
- Métricas
- Eventos
- Rastreabilidade

---

# 13. Escalabilidade

A plataforma deverá suportar:

- Multiempresa
- Multiusuário
- Multiambiente
- Alta disponibilidade
- Execução distribuída
- Filas
- Cache
- Processamento paralelo

---

# 14. Tecnologias

Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic

Banco

- PostgreSQL

Fila

- Redis
- Celery

Frontend

- React
- Vite
- Tailwind

---

# 15. Estrutura do Projeto

```
backend/
frontend/
docker/
docs/
scripts/

backend/app/

api/
core/
database/
dependencies/
exceptions/
middleware/
models/
repositories/
schemas/
services/
scanners/
workers/
utils/
ai/
```

Esta estrutura deverá permanecer estável durante toda a evolução do projeto.

---

# 16. Arquitetura dos Scanners

```
Scan Engine

↓

Providers

↓

Signals

↓

Correlation Engine

↓

Findings
```

Os scanners apenas coletam informações.

Toda inteligência pertence às camadas superiores.

---

# 17. Roadmap Arquitetural

v0.1

- Plataforma Base

v0.2

- Scan Engine

v0.3

- Threat Intelligence

v0.4

- Artificial Intelligence

v1.0

- Plataforma Enterprise

---

# 18. Decisões Arquiteturais

As decisões permanentes deverão ser registradas em:

docs/DECISIONS.md

Nenhuma decisão arquitetural relevante deverá existir apenas em conversas.

---

# 19. Considerações Finais

A arquitetura do Mouse IA deverá priorizar simplicidade, modularidade, escalabilidade e segurança.

A implementação deverá sempre seguir este documento.

Em caso de conflito entre código e arquitetura, a arquitetura possui prioridade.