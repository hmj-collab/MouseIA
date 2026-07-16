# Mouse IA — Changelog v0.2
**Versão:** v0.2  
**Status:** Release Architecture Migration  
**Tipo:** Major Architectural Evolution  

---

# Visão Geral
A versão v0.2 representa a evolução arquitetural do Mouse IA de uma aplicação funcional de análise de websites para uma plataforma SaaS de Gestão de Superfície de Ataque (Attack Surface Management).

Esta release estabelece a fundação necessária para operação multi-tenant, permitindo que múltiplas organizações utilizem a plataforma com isolamento de dados, controle de acesso e arquitetura preparada para escala Enterprise.

A principal mudança conceitual desta versão é:

Antes:

Ferramenta de Scanner Web

Depois:

Plataforma SaaS de Segurança

A v0.2 não representa apenas uma evolução técnica.

Ela representa a mudança de categoria do produto:

Ferramenta de análise pontual
↓
Plataforma de gerenciamento contínuo de superfície de ataque

---

# Marco Arquitetural

A v0.2 estabelece oficialmente o novo modelo de domínio do Mouse IA:

Organization
      |
   Project
      |
    Asset
      |
    Scan
      |
Finding / Vulnerability

Este modelo substitui a estrutura inicial:

Company
      |
    Site
      |
    Asset

A separação das responsabilidades permite que a plataforma evolua para diferentes tipos de análise de segurança sem depender exclusivamente de websites.

---

# Objetivos

Os objetivos principais desta release foram:

1. Alinhar implementação e documentação arquitetural

Garantir que o código siga os princípios definidos nos documentos:

* ARCHITECTURE.md;
* AGENT.md;
* DOMAIN.md;
* SECURITY.md;
* DECISIONS.md.

A documentação passa a ser a fonte de verdade da aplicação.

---

2. Implementar arquitetura SaaS Multi-Tenant

Criar uma base segura para múltiplos clientes utilizando a mesma plataforma.

Cada cliente deve possuir:

* seus usuários;
* suas organizações;
* seus projetos;
* seus ativos;
* seus resultados de análise.

---

3. Separar responsabilidades do domínio

Remover entidades híbridas e criar uma modelagem mais limpa:

Organization
Responsável pelo cliente
Project
Responsável pelo contexto operacional
Asset
Responsável pelo recurso técnico monitorado

---

4. Preparar o produto para escala Enterprise

Criar fundamentos para futuras capacidades:

* RBAC avançado;
* SSO;
* auditoria;
* processamento distribuído;
* integrações corporativas.

---

# Mudanças

---

1. Novo Modelo de Domínio

Modelo anterior

Company
↓
Site
↓
Asset

O modelo inicial possuía responsabilidades misturadas.

A entidade Site representava:

* agrupamento operacional;
* recurso monitorado;
* origem da execução dos scans.

---

# Novo modelo

Organization
↓
Project
↓
Asset

Cada entidade passa a possuir responsabilidade específica.

---

# Organization

Representa o tenant dentro da plataforma.

Responsabilidades:

* isolamento de dados;
* agrupamento de usuários;
* controle de acesso;
* governança.

---

# Project

Representa o contexto operacional onde os ativos estão inseridos.

Exemplos:

* aplicação institucional;
* ambiente produtivo;
* sistema interno;
* produto digital.

---

# Asset

Representa o recurso técnico monitorado.

Exemplos:

* web application;
* domínio;
* API;
* repositório;
* serviço cloud.

---

2. Migração Company → Organization

# A entidade:

Company

foi substituída por:

Organization

Alterações realizadas:

* modelos SQLAlchemy;
* schemas Pydantic;
* repositories;
* services;
* endpoints FastAPI;
* componentes frontend.

# Novo padrão:

Antes:

/companies

Depois:

/organizations

---

3. Introdução da Entidade Project

A v0.2 introduz oficialmente a entidade Project.

Responsabilidade:

Ser o container operacional dos recursos monitorados.

Exemplo:

Organization:
HMJ Fotografia
Project:
Website Institucional
Assets:
- domínio principal
- aplicação web
- API

---

4. Transformação Site → Project + Asset

Durante a análise arquitetural foi identificado que a entidade Site possuía responsabilidade híbrida.

Ela representava:

Container operacional
+
Recurso monitorado

A migração separa esses conceitos:

Site
↓
Project
+
Asset

Exemplo:

Antes:

{
"name":"HMJ Fotografia",
"url":"https://hmjfotografia.com/"
}

Depois:

Project:
HMJ Fotografia
Asset:
HMJ Fotografia Web Application
Type:
web_application

---

5. Migração e Preservação Histórica

A migração arquitetural foi planejada para preservar dados existentes.

Dados mantidos:

* usuários;
* organizações;
* projetos;
* ativos;
* scans;
* logs;
* sinais;
* findings;
* vulnerabilidades;
* recomendações.

# Princípio:

Nenhuma evidência de segurança deve ser perdida durante uma alteração arquitetural.

---

6. Evolução da API

A API foi ajustada para refletir o novo domínio.

Endpoints antigos

/companies
/sites

Novos endpoints

/organizations
/projects

---

# Assets

Antes:

{
"site_id":1
}

Depois:

{
"project_id":1
}

---

# Scans

Antes:

{
"site_id":1
}

Depois:

{
"project_id":1,
"asset_id":1
}

---

7. Evolução do Frontend

A interface foi atualizada para representar a arquitetura SaaS.

# Antes:

Empresas
Sites
Scans

# Depois:

Organizações
Projetos
Ativos
Scans
Riscos

# Alterações:

* navegação;
* componentes;
* modelos;
* chamadas API;
* contexto de usuário.

---

8. Evolução do Scan Engine

O motor de análise foi desacoplado da entidade Site.

# Modelo anterior:

Scan
↓
Site.url
↓
Scanner

# Novo modelo:

Scan
↓
Asset
↓
Asset Type
↓
Scanner Especializado

# Benefícios:

* arquitetura extensível;
* novos tipos de scanner;
* menor acoplamento;
* preparação para ASM.

---

9. Preparação Enterprise

A v0.2 prepara a plataforma para evolução futura.

Processamento distribuído

Preparação para:

Celery
+ 
Redis

---

# Banco Enterprise

Preparação para:

PostgreSQL

---

# Segurança avançada

Preparação para:

* RBAC avançado;
* SSO;
* MFA;
* auditoria;
* billing.

---

# Breaking Changes

---

# API

Endpoints removidos:

/companies
/sites

Substituídos por:

/organizations
/projects

---

# Modelo de Dados

Alterações:

Removidos:

company_id
site_id

Substituídos por:

organization_id
project_id

---

# Estrutura de Relacionamento

Antes:

Company
↓
Site
↓
Asset

Depois:

Organization
↓
Project
↓
Asset

---

# Segurança

A v0.2 introduz melhorias fundamentais de segurança.

# Implementado:

* isolamento lógico entre clientes;
* validação de acesso por tenant;
* controle de recursos por contexto;
* preparação para RBAC Enterprise.

# Regra fundamental:

Usuário A
não pode acessar
dados da Organização B

---

# Compatibilidade

A versão v0.2 mantém compatibilidade histórica com:

* dados existentes;
* registros operacionais;
* scans realizados;
* vulnerabilidades encontradas;
* evidências coletadas;
* recomendações geradas.

A migração deve preservar:

* IDs históricos;
* relacionamentos válidos;
* rastreabilidade.

---

# Critérios de Sucesso

A v0.2 é considerada concluída quando:

---

# Arquitetura

✅ Organization é o tenant root.

✅ Project é o container operacional.

✅ Asset é o recurso monitorado.

---

# Segurança

✅ Multi-tenancy implementado.

✅ Dados isolados por organização.

✅ Controle de acesso validado.

---

# API

✅ Endpoints refletem o novo domínio.

✅ Contratos atualizados.

---

# Frontend

✅ Interface representa o modelo SaaS.

✅ Fluxos principais funcionando.

---

# Scan Engine

✅ Execução baseada em Asset.

✅ Arquitetura preparada para novos scanners.

---

# Próximos Passos

A evolução prevista para a próxima versão:

v0.3

# Possíveis entregas:

PostgreSQL
Celery + Redis
RBAC avançado
Dashboard Executivo
Auditoria
Gestão de Usuários
Planos SaaS
Billing
Integrações externas
Relatórios Enterprise

---

# Conclusão

A versão v0.2 representa o nascimento da arquitetura SaaS do Mouse IA.

O produto deixa de ser uma ferramenta isolada de análise técnica e passa a possuir uma fundação preparada para operar como uma plataforma profissional de segurança.

A arquitetura agora permite crescimento mantendo:

* segurança;
* isolamento;
* escalabilidade;
* governança;
* extensibilidade.

A partir desta versão, o Mouse IA possui uma base arquitetural compatível com uma plataforma moderna de Attack Surface Management.