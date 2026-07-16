# 005-assets.md

```markdown
# Task 005 — Assets

**Release:** v0.1 — Foundation

**Epic:** Gestão de Plataforma

**Status:** Ready

**Prioridade:** Alta

---

# Objetivo

Implementar e consolidar o módulo de Assets como a entidade responsável por representar os recursos tecnológicos monitorados pela plataforma Mouse IA.

Um Asset representa um recurso pertencente a um Project que poderá futuramente ser analisado, monitorado e correlacionado através de Scans, Providers, Signals e Findings.

O objetivo desta Task é criar uma estrutura flexível e extensível capaz de representar diferentes tipos de ativos de segurança mantendo rastreabilidade, isolamento e compatibilidade com a arquitetura oficial.

---

# Contexto

Dentro da arquitetura do Mouse IA, Assets representam os objetos reais existentes no ambiente de uma Organization.

Exemplos:

- aplicações web;
- APIs;
- domínios;
- endereços IP;
- repositórios;
- recursos Cloud;
- servidores;
- containers;
- aplicações mobile.

Um mesmo cliente poderá possuir diversos Projects e cada Project poderá possuir diversos Assets.

Hierarquia oficial:

```text
Organization

↓

Project

↓

Asset

↓

Scan

↓

Provider

↓

Signal

↓

Finding

↓

Vulnerability

↓

Recommendation

↓

Task

↓

Report
```

---

# Conceito de Domínio

Asset representa um recurso tecnológico que pertence a um Project e pode ser alvo de monitoramento de segurança.

O Asset contém informações necessárias para identificação, classificação e gerenciamento do recurso.

O Asset não representa uma vulnerabilidade.

Ele representa o objeto onde vulnerabilidades poderão ser encontradas.

---

# Responsabilidades do Asset

Um Asset é responsável por:

- manter identidade própria;
- pertencer obrigatoriamente a um Project;
- representar um recurso tecnológico;
- definir tipo de ativo;
- armazenar informações de identificação;
- manter ciclo de vida;
- fornecer contexto para futuras análises;
- permitir rastreabilidade histórica.

---

# Não Responsabilidades do Asset

O Asset NÃO deverá:

- executar Scans;
- chamar Providers;
- interpretar Signals;
- criar Findings;
- gerar Vulnerabilities;
- calcular Risk Score;
- executar Recommendations;
- corrigir problemas automaticamente.

Essas responsabilidades pertencem aos respectivos módulos da arquitetura.

---

# Estado Atual

Atualmente o projeto possui:

- Backend FastAPI operacional;
- Frontend React funcional;
- Sistema de autenticação implementado;
- Organization definida;
- Project definido;
- Estrutura inicial de banco de dados;
- Componentes iniciais de segurança.

Ainda não existe uma camada completa de gerenciamento de Assets.

Esta Task será responsável por criar a base necessária para representar recursos monitorados.

---

# Objetivos da Task

Esta Task deverá:

- Implementar a entidade Asset;
- Vincular Assets aos Projects;
- Criar CRUD completo;
- Criar regras de domínio;
- Criar Services;
- Criar Repository;
- Criar Schemas;
- Integrar Backend e Frontend;
- Preparar integração futura com Scan Engine;
- Garantir isolamento correto entre Organizations.

---

# Escopo

Inclui:

- Cadastro de Assets;
- Listagem de Assets;
- Consulta individual;
- Atualização;
- Exclusão lógica;
- Classificação por tipo;
- Controle de ciclo de vida;
- Associação obrigatória com Project;
- Validações;
- Testes;
- Documentação.

---

# Fora do Escopo

Esta Task NÃO deverá implementar:

- Execução de Scans;
- Providers;
- HTTP Discovery;
- Nmap;
- WhatWeb;
- Signals;
- Findings;
- Vulnerabilities;
- Correlation Engine;
- Threat Intelligence;
- Risk Engine;
- Remediação automática.

Essas funcionalidades pertencem a Releases futuras.

---

# Arquitetura Esperada

```text
Project

↓

Assets API

↓

Asset Service

↓

Asset Repository

↓

Database
```

Nenhuma regra de negócio deverá permanecer diretamente nas rotas.

As regras deverão existir exclusivamente na camada Service.

---

# Modelo Conceitual

```text
Organization

↓

Project

↓

Asset

↓

Scan

↓

Signal

↓

Finding

↓

Vulnerability
```

Um Asset sempre deverá existir dentro do contexto de um Project.

---

# Tipos de Assets

O modelo deverá permitir diferentes categorias de ativos.

Tipos esperados:

```text
domain
ip_address
web_application
api
repository
cloud_resource
server
container
mobile_application
other
```

Novos tipos poderão ser adicionados futuramente.

---

# Modelo de Dados Esperado

A entidade Asset deverá possuir:

## Identificação

- ID;
- UUID;
- Project ID;
- Nome;
- Tipo;
- Valor principal.

## Contexto

- Descrição;
- Ambiente;
- Criticidade;
- Status.

## Controle

- Data de criação;
- Data de atualização;
- Data de exclusão lógica.

---

# Campos Esperados

Exemplo:

```text
Asset

id
uuid
project_id
name
asset_type
value
description
environment
criticality
status
created_at
updated_at
deleted_at
```

Campos adicionais poderão ser incluídos desde que estejam alinhados ao domínio.

---

# Valores Permitidos

## Environment

Valores esperados:

```text
production
staging
development
testing
sandbox
unknown
```

---

## Criticality

Valores esperados:

```text
low
medium
high
critical
```

---

## Status

Valores esperados:

```text
active
deprecated
retired
archived
```

---

# Regras de Negócio

Um Asset:

- deverá possuir Project válido;
- não poderá existir sem Project;
- deverá possuir nome obrigatório;
- deverá possuir tipo definido;
- deverá possuir valor identificador;
- deverá possuir ciclo de vida;
- não poderá acessar dados de outro Project;
- deverá respeitar isolamento da Organization;
- deverá permitir exclusão lógica.

---

# Regras de Isolamento

Toda operação envolvendo Assets deverá respeitar a hierarquia:

```text
Organization

↓

Project

↓

Asset
```

Nenhum Asset poderá ser consultado, alterado ou removido fora do contexto do Project e Organization proprietários.

---

# Exclusão Lógica

Assets não deverão ser removidos fisicamente.

A remoção deverá utilizar Soft Delete.

Campos esperados:

```text
deleted_at

deleted_by
```

Objetivos:

- preservar histórico;
- manter rastreabilidade;
- evitar perda de informações de segurança.

---

# API Esperada

Endpoints:

```text
GET     /assets

GET     /assets/{id}

POST    /assets

PUT     /assets/{id}

DELETE  /assets/{id}
```

Consulta por Project:

```text
GET /projects/{project_id}/assets
```

---

# Estrutura Esperada

```text
backend/app/

api/
    assets.py

models/
    asset.py

repositories/
    asset_repository.py

schemas/
    asset.py

services/
    asset_service.py
```

A estrutura poderá evoluir desde que siga a arquitetura oficial.

---

# Integração Frontend

O Frontend deverá permitir:

- visualizar Assets;
- criar Assets;
- editar Assets;
- remover Assets;
- visualizar tipo;
- visualizar ambiente;
- visualizar criticidade;
- visualizar status.

A interface deverá permanecer consistente com os módulos existentes.

---

# Requisitos Funcionais

O sistema deverá permitir:

- Criar Assets;
- Editar Assets;
- Listar Assets;
- Consultar Asset individual;
- Filtrar Assets por Project;
- Validar dados de entrada;
- Remover Assets logicamente.

---

# Requisitos Não Funcionais

Toda implementação deverá seguir:

- Clean Architecture;
- SOLID;
- DRY;
- KISS;
- Security First;
- Fail Fast.

Todo código deverá possuir:

- Type Hints;
- Docstrings;
- Tratamento de exceções;
- Logs estruturados.

---

# Segurança

Os endpoints deverão exigir autenticação.

As validações deverão impedir:

- acesso entre Organizations;
- acesso entre Projects;
- criação de Asset sem contexto válido;
- exposição indevida de informações;
- operações inválidas.

---

# Preparação Futura

O modelo de Asset deverá permitir evolução para:

- descoberta automática;
- integração com Providers;
- monitoramento contínuo;
- relacionamento com Findings;
- cálculo de risco;
- inventário de segurança.

Essas funcionalidades não fazem parte desta Task.

---

# Estratégia de Migração

Caso exista implementação parcial:

- preservar comportamento existente;
- manter compatibilidade com Frontend;
- evitar mudanças disruptivas;
- realizar evolução incremental.

---

# Critérios de Aceite

Esta Task será considerada concluída quando:

- CRUD funcional;
- Asset vinculado obrigatoriamente a Project;
- Endpoints documentados;
- Service implementado;
- Repository implementado;
- Schemas implementados;
- Frontend integrado;
- Validações concluídas;
- Testes executados;
- Isolamento entre Organizations garantido.

---

# Critérios de Qualidade

Todo código deverá:

- ser modular;
- ser desacoplado;
- ser documentado;
- ser testável;
- seguir AGENT.md;
- seguir ARCHITECTURE.md;
- respeitar DECISIONS.md.

---

# Dependências

Documentação obrigatória:

- docs/ARCHITECTURE.md
- docs/AGENT.md
- docs/ROADMAP.md
- docs/SECURITY.md
- docs/DECISIONS.md

Dependências técnicas:

- Task 001 — Bootstrap
- Task 002 — Authentication
- Task 003 — Organizations
- Task 004 — Projects

---

# Definition of Done

A Task será considerada concluída quando:

- Todos os critérios de aceite forem atendidos;
- Assets estiverem vinculados corretamente aos Projects;
- O isolamento multi-tenant estiver preservado;
- Backend e Frontend permanecerem compatíveis;
- A arquitetura permanecer preservada;
- A documentação estiver consistente.

---

# Próxima Task

Após a conclusão desta Task deverá ser iniciada:

**Release v0.2 — Scan Engine**

Próximas etapas:

- Scan Engine;
- Providers;
- HTTP Discovery;
- Nmap Provider;
- WhatWeb Provider.

O Scan Engine utilizará Assets como entrada principal para execução de análises.
```
