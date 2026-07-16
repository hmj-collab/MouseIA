# Task 004 — Projects

**Release:** v0.1 — Foundation

**Epic:** Gestão de Plataforma

**Status:** Ready

**Prioridade:** Alta

---

# Objetivo

Implementar e consolidar o módulo de Projects como uma entidade central da plataforma Mouse IA.

Um Project representa uma unidade operacional de segurança pertencente obrigatoriamente a uma Organization.

O Project será responsável por fornecer contexto para gerenciamento de ativos, monitoramento, análises e operações de segurança.

O objetivo desta Task é criar uma estrutura preparada para representar diferentes ambientes, sistemas, aplicações ou unidades operacionais de uma mesma empresa, mantendo isolamento, rastreabilidade e compatibilidade com a arquitetura oficial da plataforma.

---

# Contexto

Uma Organization poderá possuir diversos Projects.

Cada Project representa um contexto independente de operação dentro da plataforma.

Exemplos:

- Internet Banking;
- Aplicação Mobile;
- API Corporativa;
- Ambiente Cloud;
- Portal Institucional;
- Sistemas internos.

Toda operação executada pelo Mouse IA deverá ocorrer dentro do contexto de uma Organization e, quando aplicável, de um Project.

O Project permitirá que uma mesma empresa monitore diferentes ambientes sem mistura de informações.

---

# Conceito de Domínio

Project é uma unidade operacional de segurança dentro de uma Organization.

Ele representa o contexto onde ativos serão monitorados e analisados.

Um Project possui informações relevantes para interpretação futura de riscos, como:

- ambiente;
- criticidade;
- descrição operacional;
- responsáveis;
- ciclo de vida.

O Project não representa uma vulnerabilidade, scan ou finding.

Ele apenas fornece contexto para essas entidades.

---

# Responsabilidades do Project

Um Project é responsável por:

- manter identidade própria;
- pertencer a uma Organization;
- organizar Assets relacionados;
- fornecer contexto operacional;
- definir ambiente;
- definir criticidade;
- manter ciclo de vida;
- permitir rastreabilidade histórica.

---

# Não Responsabilidades do Project

O Project NÃO deverá:

- executar Scans;
- chamar Providers;
- interpretar Signals;
- criar Findings;
- gerar Vulnerabilities;
- calcular Risk Score;
- executar Recommendations;
- realizar ações automatizadas.

Essas responsabilidades pertencem aos respectivos módulos da arquitetura.

---

# Estado Atual

Atualmente o projeto possui:

- Backend FastAPI operacional;
- Frontend React funcional;
- Sistema de autenticação implementado;
- Estrutura inicial de banco de dados;
- Dashboard funcional;
- Arquitetura definida;
- Módulo Organizations implementado ou em desenvolvimento.

Até o momento não existe um módulo completo para gerenciamento de Projects.

Esta Task será responsável por criar ou consolidar esse módulo mantendo compatibilidade com a estrutura existente.

---

# Objetivos da Task

Esta Task deverá:

- Implementar a entidade Project;
- Vincular Projects às Organizations;
- Criar CRUD completo;
- Implementar regras de domínio;
- Criar Services;
- Criar Repository;
- Criar Schemas;
- Integrar Backend e Frontend;
- Preparar a plataforma para Assets;
- Garantir isolamento correto entre Organizations.

---

# Escopo

Inclui:

- Cadastro de Projects;
- Listagem de Projects;
- Consulta individual;
- Atualização;
- Exclusão lógica;
- Associação obrigatória com Organization;
- Validações;
- Regras de negócio;
- Testes;
- Documentação.

---

# Fora do Escopo

Esta Task NÃO deverá implementar:

- Assets;
- Scans;
- Providers;
- Signals;
- Findings;
- Vulnerabilities;
- Risk Engine;
- Threat Intelligence;
- Dashboard avançado;
- RBAC completo;
- Compartilhamento entre usuários;
- Billing;
- Auditoria avançada.

Essas funcionalidades pertencem a futuras Releases.

---

# Arquitetura Esperada

```text
Organization

↓

Projects API

↓

Project Service

↓

Project Repository

↓

Database