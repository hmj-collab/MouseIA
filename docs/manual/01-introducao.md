# Capítulo 1: Introdução e Arquitetura

## 1. Visão Geral do Mouse IA
O **Mouse IA** é uma plataforma profissional de **Attack Surface Management (ASM)**, **Vulnerability Management (VM)** e **AI Security Analytics**. O seu objetivo principal é consolidar evidências técnicas e atuar como um orquestrador central que:
* Mapeia a superfície de ataque externa (alvos web, portas expostas, assinaturas de software).
* Correlaciona sinais brutos em vulnerabilidades inteligíveis através de motores de regra.
* Enriquece dados utilizando Threat Intelligence em tempo real (CVSS, EPSS e catálogo CISA KEV de explorações ativas).
* Avalia e mitiga achados com Inteligência Artificial, gerando guias de hardening, resumos de impacto comercial e detecção automática de falsos positivos.

---

## 2. Tecnologias Utilizadas

### Backend
* **Python 3.9+** como linguagem de desenvolvimento.
* **FastAPI** para a disponibilização de endpoints REST rápidos, assíncronos e autodeclarativos (OpenAPI).
* **SQLAlchemy** como ORM (Object-Relational Mapping) para controle e persistência de dados.
* **Alembic** para versionamento de migrações do banco de dados.
* **Pydantic v2** para validação e serialização de dados de entrada/saída.
* **Pytest** para a suíte completa de testes unitários e de integração.

### Banco de Dados
* **SQLite:** Utilizado como banco de desenvolvimento local por sua simplicidade.
* **PostgreSQL:** Suporte nativo para ambientes de produção.

### Frontend
* **React 18** estruturado de forma reativa e modular.
* **Vite** como bundler ultrarrápido para desenvolvimento e builds de produção.
* **Lucide React** para iconografia técnica moderna.
* **CSS Puro (Vanilla CSS):** Customização premium sem dependência pesada de frameworks utilitários como TailwindCSS, mantendo flexibilidade total no layout.

---

## 3. Padrões de Arquitetura (Clean Architecture)
A arquitetura do Mouse IA segue o padrão de desacoplamento de camadas, garantindo manutenibilidade e extensibilidade:

```
┌─────────────────────────────────────────────────────────┐
│                       FRONTEND                          │
│                    (React + Vite)                       │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP REST
                           ▼
┌─────────────────────────────────────────────────────────┐
│                       API ROUTES                        │
│                   (FastAPI Controllers)                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    SERVICES LAYER                       │
│        (Scan, Correlation, ThreatIntel, AI Services)    │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  REPOSITORIES LAYER                     │
│           (Project, Asset, Vulnerability Repos)         │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   DATABASE / MODELS                     │
│                 (SQLite/PostgreSQL)                     │
└─────────────────────────────────────────────────────────┘
```

* **API Controllers (app/api):** Apenas expõem e direcionam as rotas, validando permissões (RBAC) e schemas de entrada.
* **Services (app/services):** Onde reside a lógica de negócios complexa, como o agrupamento temporal de sinais e chamada de APIs de IA.
* **Repositories (app/repositories):** Fazem a ponte entre a lógica de negócios e as consultas cruas de persistência de banco de dados.
* **Models (app/models):** Declaração das tabelas e relacionamentos SQLAlchemy.
