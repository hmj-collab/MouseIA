# Mouse IA

> **Attack Surface Management (ASM) • Vulnerability Management (VM) • Threat Intelligence • AI Security Analytics**

Mouse IA é uma plataforma profissional para descoberta, análise, correlação e gestão inteligente de vulnerabilidades em ativos digitais.

Diferente de ferramentas tradicionais de segurança, o Mouse IA não pretende substituir scanners especializados como **Nmap**, **Nuclei**, **WPScan** ou **WhatWeb**.

Seu objetivo é orquestrar essas ferramentas, normalizar evidências técnicas, correlacionar informações, enriquecer resultados utilizando Threat Intelligence e Inteligência Artificial e transformar milhares de dados técnicos em decisões acionáveis para equipes de Cyber Security, DevSecOps, Infraestrutura e Desenvolvimento.

---

# Status do Projeto

**Versão:** v0.1 — Foundation

**Situação:**

- ✅ Arquitetura definida
- ✅ Backend FastAPI
- ✅ Frontend React + Vite
- ✅ Autenticação JWT
- ✅ Organizations
- ✅ Projects
- ✅ Assets
- ✅ Scan Pipeline Inicial
- 🚧 Scan Engine Modular
- 🚧 Threat Intelligence
- 🚧 Correlation Engine
- 🚧 AI Engine
- 🚧 Dashboard Executivo

---

# Visão

O Mouse IA foi projetado para ser uma plataforma Enterprise capaz de acompanhar todo o ciclo de vida da gestão de vulnerabilidades.

Seu fluxo principal é composto por:

```text
Organization
      │
      ▼
 Project
      │
      ▼
  Asset
      │
      ▼
 Scan Engine
      │
      ▼
 Providers
      │
      ▼
 Signals
      │
      ▼
Correlation Engine
      │
      ▼
 Findings
      │
      ▼
Threat Intelligence
      │
      ▼
Vulnerabilities
      │
      ▼
 AI Engine
      │
      ▼
Recommendations
      │
      ▼
   Tasks
      │
      ▼
  Reports
```

---

# Principais Recursos

## Gestão

- Organizations
- Projects
- Assets
- Usuários
- Permissões
- RBAC

---

## Scan Engine

Motor responsável pela orquestração dos scanners.

Suporte planejado para:

- HTTPX
- Nmap
- Nuclei
- WhatWeb
- WPScan
- Katana
- Naabu
- DNSX
- SSLyze
- TestSSL
- Nikto
- CMSeeK

---

## Correlation Engine

Responsável por transformar Signals em Findings.

---

## Threat Intelligence

Integração planejada com:

- NVD
- CISA KEV
- EPSS
- OSV
- GitHub Advisories
- WordPress.org
- VulnCheck
- OTX

---

## Artificial Intelligence

A IA será responsável por:

- Priorização de riscos
- Explicação de vulnerabilidades
- Recomendações
- Identificação de possíveis falsos positivos
- Resumos executivos
- Apoio à tomada de decisão

---

## Dashboard

Planejado para oferecer:

- Dashboard Executivo
- Dashboard Técnico
- Histórico
- Evolução
- Tendências
- KPIs

---

# Arquitetura

O Mouse IA utiliza uma arquitetura modular baseada em Clean Architecture.

```text
Frontend

↓

API

↓

Application

↓

Domain

↓

Infrastructure

↓

Providers

↓

Threat Intelligence

↓

Artificial Intelligence
```

Toda regra de negócio permanece desacoplada das ferramentas externas.

---

# Tecnologias

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic

---

## Banco de Dados

- PostgreSQL (Produção)
- SQLite (Desenvolvimento)

---

## Frontend

- React
- Vite
- Tailwind CSS

---

## Infraestrutura

- Docker
- Redis
- Celery

---

## Testes

- Pytest

---

# Instalação

## Backend

```bash
cd backend

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Estrutura do Projeto

```text
MouseIA/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── scanners/
│   │   ├── workers/
│   │   ├── ai/
│   │   └── utils/
│   ├── alembic/
│   └── tests/
│
├── frontend/
│
├── docs/
│
├── scripts/
│
├── tasks/
│
├── LICENSE
│
└── README.md
```

---

# Roadmap

## v0.1

Foundation

- Plataforma Base
- Backend
- Frontend
- Organizations
- Projects
- Assets

---

## v0.2

Scan Platform

- Scan Engine
- Scheduler
- Providers

---

## v0.3

Threat Intelligence

- Correlation Engine
- Vulnerability Intelligence
- Risk Score

---

## v0.4

Artificial Intelligence

- AI Engine
- Recommendations
- False Positive Analysis

---

## v0.5

Reporting

- Dashboard Executivo
- Dashboard Técnico
- Relatórios
- Exportações

---

## v1.0

Enterprise Ready

- API Pública
- Multiempresa
- Escalabilidade
- Documentação Completa
- Alta Disponibilidade

---

# Documentação

Toda a documentação oficial encontra-se na pasta **docs/**.

- ARCHITECTURE.md
- AGENT.md
- ROADMAP.md
- SIGNALS.md
- SECURITY.md
- DECISIONS.md
- CHANGELOG.md

---

# Filosofia

O Mouse IA não busca possuir o maior número de funcionalidades.

Seu objetivo é integrar ferramentas consolidadas de segurança em uma única plataforma capaz de transformar evidências técnicas em inteligência acionável.

A plataforma foi projetada para ser:

- Modular
- Escalável
- Segura
- Extensível
- Orientada a Dados
- Preparada para Inteligência Artificial

Toda evolução deverá preservar a arquitetura definida no projeto.

---

# Contribuindo

Contribuições são bem-vindas.

Antes de iniciar qualquer desenvolvimento:

1. Leia `docs/AGENT.md`.
2. Leia `docs/ARCHITECTURE.md`.
3. Consulte `docs/ROADMAP.md`.
4. Escolha uma Task correspondente à Release em desenvolvimento.
5. Siga os padrões arquiteturais definidos para o projeto.

---

# Licença

Este projeto está licenciado conforme o arquivo **LICENSE**.

---

# Autor

**Henry M Jr**

Analista de Sistemas | Cyber Security | DevSecOps | Software Architecture

Projeto desenvolvido com foco em criar uma plataforma moderna de gestão inteligente de vulnerabilidades, preparada para ambientes corporativos e evolução contínua.