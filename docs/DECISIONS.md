# DECISIONS.md

# Mouse IA - Architecture Decision Records (ADR)

**Versão:** 1.0  
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
|----------|------------|
| Draft | Em discussão |
| Accepted | Aprovada |
| Implemented | Implementada |
| Deprecated | Não utilizar em novos desenvolvimentos |
| Superseded | Substituída por outra ADR |

---

# Modelo Oficial

Cada ADR deverá seguir exatamente esta estrutura.

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

---

# ADR-003

## Título

Threat Intelligence centralizada

## Status

Accepted

## Data

2026-07-16

## Contexto

Diversas bases públicas poderão ser utilizadas.

## Decisão

Toda consulta às bases externas ocorrerá exclusivamente através da camada Threat Intelligence.

## Consequências

- Código desacoplado.
- Fácil inclusão de novas fontes.
- Cache centralizado.

## Alternativas Consideradas

Cada scanner consultar CVEs.

Rejeitada.

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

- Signals
- Findings
- Vulnerabilities

A IA nunca executará ferramentas externas.

## Consequências

Separação clara entre coleta e análise.

---

# ADR-005

## Título

Arquitetura modular baseada em Providers

## Status

Accepted

## Data

2026-07-16

## Contexto

O Mouse IA deverá integrar dezenas de ferramentas diferentes ao longo do tempo.

## Decisão

Toda ferramenta externa deverá ser implementada como um Provider independente.

## Consequências

- Fácil manutenção.
- Fácil expansão.
- Baixo acoplamento.

---

# ADR-006

## Título

Fluxo oficial do Mouse IA

## Status

Accepted

## Data

2026-07-16

## Decisão

Todo processamento deverá seguir obrigatoriamente:

```text
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

## Consequências

Todos os módulos deverão respeitar este fluxo.

---

# ADR-007

## Título

Arquitetura prioriza domínio sobre implementação

## Status

Accepted

## Data

2026-07-16

## Contexto

O projeto deverá evoluir durante muitos anos.

Tecnologias poderão ser substituídas.

## Decisão

As regras de negócio permanecerão independentes de frameworks, bancos de dados e ferramentas externas.

## Consequências

Maior longevidade do projeto.

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

Princípios obrigatórios:

- Menor Privilégio
- Defense in Depth
- Secure Defaults
- Fail Secure
- Validação de Entrada
- Auditoria
- Logs Estruturados

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

Toda funcionalidade deverá seguir:

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

Projetos longos tendem a perder consistência quando decisões permanecem apenas em conversas.

## Decisão

A documentação oficial possui prioridade sobre o código em caso de divergência conceitual.

Os seguintes documentos compõem a fonte de verdade do projeto:

- ARCHITECTURE.md
- AGENT.md
- ROADMAP.md
- SECURITY.md
- SIGNALS.md
- DECISIONS.md

## Consequências

- Maior consistência arquitetural.
- Facilidade para onboarding de novos desenvolvedores e Agents.
- Redução de retrabalho.
- Evolução previsível da plataforma.

---

# Próximas ADRs

Novas decisões deverão ser registradas sempre que envolverem:

- Arquitetura
- Banco de Dados
- Segurança
- IA
- Threat Intelligence
- Providers
- APIs
- Escalabilidade
- Performance
- Infraestrutura
- Modelo de Dados
- Estratégias de Cache
- Estratégias de Filas
- Observabilidade

---

# Filosofia

Uma boa arquitetura não é aquela que nunca muda.

É aquela cuja evolução é documentada, compreendida e rastreável.

Cada ADR representa uma decisão consciente tomada para preservar a qualidade, a consistência e a longevidade do Mouse IA.

