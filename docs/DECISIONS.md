# DECISIONS.md

# Mouse IA - Architecture Decision Records (ADR)

**Versão:** 1.1  
**Status:** Oficial

---

# Objetivo

Este documento registra todas as decisões arquiteturais relevantes do Mouse IA.

Seu propósito é preservar o contexto das decisões tomadas durante a evolução do projeto.

Nenhuma decisão arquitetural importante deverá existir apenas em conversas, commits ou Pull Requests.

Caso uma decisão seja alterada futuramente, ela **não deverá ser removida**.

Seu status deverá ser atualizado para **Superseded**, indicando qual ADR a substituiu.

---

# Status possíveis

| Status | Significado |
|---|---|
| Draft | Em discussão |
| Accepted | Aprovada |
| Implemented | Implementada |
| Deprecated | Não utilizar em novos desenvolvimentos |
| Superseded | Substituída por outra ADR |

---

# Modelo Oficial

Cada ADR deverá seguir:

```text
ADR-XXX

Título

Status

Data

Contexto

Decisão

Consequências

Alternativas Consideradas

Observações
```

---

# ADR-001

## Título

Separação entre Signals e Findings

## Status

Accepted

## Data

2026-07-16

## Contexto

Ferramentas de segurança normalmente misturam evidências técnicas com vulnerabilidades.

Isso dificulta correlação, enriquecimento e reutilização das informações.

## Decisão

O Mouse IA utilizará dois conceitos independentes.

Signals representam fatos observados.

Findings representam interpretações realizadas sobre um ou mais Signals.

## Consequências

- Melhor desacoplamento.
- Correlação mais eficiente.
- Melhor suporte à IA.
- Reutilização dos Signals.

## Alternativas Consideradas

Criar vulnerabilidades diretamente a partir dos scanners.

Rejeitada.

## Observações

Signals nunca representam vulnerabilidades.

---

# ADR-002

## Título

Providers não possuem regra de negócio

## Status

Accepted

## Data

2026-07-16

## Contexto

Ferramentas como Nmap, Nuclei e WPScan produzem informações técnicas.

Misturar inteligência nesses módulos aumenta o acoplamento.

## Decisão

Providers apenas executam ferramentas externas e convertem resultados para Signals.

Toda inteligência pertence às camadas superiores.

## Consequências

- Providers simples.
- Fácil manutenção.
- Fácil substituição de ferramentas.

## Alternativas Consideradas

Cada Provider interpretar seus próprios resultados.

Rejeitada.

## Observações

Providers não devem criar Findings ou Vulnerabilities.

---

# ADR-003

## Título

Threat Intelligence centralizada

## Status

Accepted

## Data

2026-07-16

## Contexto

Diversas bases públicas poderão ser utilizadas para enriquecimento de vulnerabilidades.

## Decisão

Toda consulta às bases externas ocorrerá exclusivamente através da camada Threat Intelligence.

## Consequências

- Código desacoplado.
- Fácil inclusão de novas fontes.
- Cache centralizado.
- Histórico de enriquecimento.

## Alternativas Consideradas

Cada scanner consultar CVEs diretamente.

Rejeitada.

## Observações

Threat Intelligence complementa Findings, não substitui evidências técnicas.

---

# ADR-004

## Título

A Inteligência Artificial nunca executa scanners

## Status

Accepted

## Data

2026-07-16

## Contexto

A IA possui finalidade analítica.

## Decisão

A IA receberá apenas:

- Signals;
- Findings;
- Vulnerabilities.

A IA nunca executará ferramentas externas.

A IA também nunca deverá:

- executar ações destrutivas;
- alterar produção sem aprovação;
- tomar decisões críticas sem justificativa.

## Consequências

Separação clara entre coleta, análise e execução.

## Alternativas Consideradas

Permitir que a IA execute ferramentas automaticamente.

Rejeitada.

---

# ADR-005

## Título

Arquitetura modular baseada em Providers

## Status

Accepted

## Data

2026-07-16

## Contexto

O Mouse IA deverá integrar dezenas de ferramentas diferentes.

## Decisão

Toda ferramenta externa deverá ser implementada como um Provider independente.

## Consequências

- Fácil manutenção.
- Fácil expansão.
- Baixo acoplamento.

## Alternativas Consideradas

Cada scanner possuir sua própria lógica de negócio.

Rejeitada.

---

# ADR-006

## Título

Fluxo oficial do Mouse IA

## Status

Accepted

## Data

2026-07-16

## Decisão

Todo processamento deverá seguir:

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

Correlation Engine

↓

Finding

↓

Threat Intelligence

↓

Vulnerability

↓

AI Engine

↓

Recommendation

↓

Task

↓

Report
```

## Consequências

Todos os módulos deverão respeitar este fluxo.

## Observações

Nenhuma camada deverá pular responsabilidades.

---

# ADR-007

## Título

Arquitetura prioriza domínio sobre implementação

## Status

Accepted

## Data

2026-07-16

## Contexto

Tecnologias podem mudar durante a evolução do produto.

## Decisão

As regras de negócio permanecerão independentes de frameworks, bancos de dados e ferramentas externas.

## Consequências

Maior longevidade da plataforma.

---

# ADR-008

## Título

Segurança por padrão (Security by Design)

## Status

Accepted

## Data

2026-07-16

## Decisão

Toda funcionalidade deverá considerar segurança desde sua concepção.

Princípios:

- Menor Privilégio.
- Defense in Depth.
- Secure Defaults.
- Fail Secure.
- Validação de Entrada.
- Auditoria.
- Logs Estruturados.

---

# ADR-009

## Título

Desenvolvimento orientado por Releases, Épicos e Tasks

## Status

Accepted

## Data

2026-07-16

## Decisão

Nenhuma implementação poderá ocorrer diretamente.

Fluxo:

```text
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

# ADR-010

## Título

Documentação como Fonte de Verdade

## Status

Accepted

## Data

2026-07-16

## Contexto

Projetos longos perdem consistência quando decisões permanecem apenas em conversas.

## Decisão

A documentação oficial possui prioridade sobre o código em caso de divergência conceitual.

Documentos oficiais:

- ARCHITECTURE.md
- AGENT.md
- DECISIONS.md
- DOMAIN.md
- ROADMAP.md
- SECURITY.md
- SIGNALS.md

## Consequências

- Maior consistência arquitetural.
- Melhor onboarding.
- Menor retrabalho.

---

# ADR-011

## Título

Isolamento Multi-Tenant por Organization

## Status

Accepted

## Data

2026-07-16

## Contexto

O Mouse IA será uma plataforma SaaS utilizada por múltiplas empresas.

## Decisão

Toda informação operacional deverá respeitar:

```text
Organization

↓

Project

↓

Asset

↓

Scan
```

Nenhuma consulta poderá retornar dados fora do contexto autorizado.

## Consequências

- Segurança entre tenants.
- Controle de acesso previsível.
- Preparação para Enterprise.

## Alternativas Consideradas

Separação apenas por filtros de frontend.

Rejeitada.

## Observações

O isolamento deve existir no backend.

---

# ADR-012

## Título

Separação entre Authentication e Authorization

## Status

Accepted

## Data

2026-07-16

## Contexto

Identidade e permissão possuem responsabilidades diferentes.

## Decisão

Authentication responde:

"Quem é o usuário?"

Authorization responde:

"O que o usuário pode acessar?"

## Consequências

Permite evolução futura para:

- RBAC;
- MFA;
- SSO;
- permissões por Organization;
- permissões por Project.

## Alternativas Consideradas

Misturar autenticação e autorização.

Rejeitada.

---

# ADR-013

## Título

Exclusão lógica de entidades operacionais

## Status

Accepted

## Data

2026-07-16

## Contexto

Em Cyber Security, histórico possui valor de evidência.

## Decisão

Entidades operacionais críticas utilizarão exclusão lógica.

Exemplos:

- Organization;
- Project;
- Asset;
- Scan;
- Finding.

## Consequências

- Preservação histórica.
- Auditoria.
- Recuperação de dados.

## Alternativas Consideradas

Exclusão física definitiva.

Rejeitada.

---

# ADR-014

## Título

Separação de Containers Operacionais e Recursos Monitorados

## Status

Accepted

## Data

2026-07-16

## Contexto

A entidade Site inicialmente acumulava duas responsabilidades:

- representar um agrupador operacional;
- representar um recurso técnico monitorado.

Essa abordagem limita a evolução para uma arquitetura multi-tenant escalável.

## Decisão

A entidade Site deixa de existir como conceito de domínio.

Cada Site legado será transformado em:

Project:

- representa contexto operacional;
- mantém agrupamento;
- preserva histórico.

Asset:

- representa recurso técnico;
- contém URL, domínio ou aplicação monitorada.

Durante a migração:

Cada Site existente será convertido em:

1 Project operacional.

+

1 Asset técnico correspondente.

O histórico de scans e evidências deverá ser preservado.

## Consequências

Benefícios:

- Domínio mais claro.
- Melhor isolamento multi-tenant.
- Suporte para múltiplos Assets por Project.
- Evolução para ASM.

Custos:

- Migration de dados.
- Atualização de APIs.
- Atualização do frontend.

## Alternativas Consideradas

Manter Site como entidade híbrida.

Rejeitada.

## Observações

Esta decisão deve orientar toda evolução futura do modelo Asset.

---

# ADR-015

## Título

PostgreSQL como banco de produção

## Status

Accepted

## Data

2026-07-16

## Contexto

SQLite é adequado para desenvolvimento local, porém possui limitações para concorrência e escala.

## Decisão

SQLite será utilizado somente para desenvolvimento.

Ambientes produtivos deverão utilizar PostgreSQL.

## Consequências

- Maior escalabilidade.
- Melhor concorrência.
- Maior compatibilidade Enterprise.

## Alternativas Consideradas

Utilizar SQLite em produção.

Rejeitada.

---

# ADR-016

## Título

Execução assíncrona de Scans via Workers

## Status

Accepted

## Data

2026-07-16

## Contexto

Scans podem ser operações longas e intensivas.

Executá-los dentro da API limita escalabilidade.

## Decisão

A execução de scans deverá utilizar processamento assíncrono.

Arquitetura:

```text
API

↓

Redis Queue

↓

Celery Worker

↓

Provider

↓

Signals
```

## Consequências

- Melhor escalabilidade.
- Separação entre API e processamento.
- Execuções paralelas controladas.

## Alternativas Consideradas

Executar scans diretamente no FastAPI.

Rejeitada.

---

# Próximas ADRs

Novas decisões deverão ser registradas sempre que envolverem:

- Arquitetura.
- Banco de Dados.
- Segurança.
- IA.
- Threat Intelligence.
- Providers.
- APIs.
- Escalabilidade.
- Performance.
- Infraestrutura.
- Modelo de Dados.
- Estratégias de Cache.
- Estratégias de Filas.
- Observabilidade.

---

# Filosofia

Uma boa arquitetura não é aquela que nunca muda.

É aquela cuja evolução é documentada, compreendida e rastreável.

Cada ADR representa uma decisão consciente tomada para preservar a qualidade, consistência e longevidade do Mouse IA.