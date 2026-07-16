# v0.2.008 — Frontend Refactor

## Mouse IA — SaaS Interface Alignment

**Release:** v0.2  
**Task:** 008  
**Status:** Planned  
**Tipo:** Frontend / Interface / API Integration

---

# Objetivo

Atualizar o frontend do Mouse IA para refletir o novo modelo arquitetural definido na Release v0.2.

A interface deverá deixar de representar o modelo legado baseado em:

```text
Company

    |

 Site

    |

 Scan
```

e passar a representar o domínio oficial:

```text
Organization

      |

   Project

      |

    Asset

      |

    Scan

      |

    Risk
```

---

# Princípio Fundamental

A interface do Mouse IA deve comunicar claramente o modelo SaaS:

> Cada usuário visualiza somente os recursos pertencentes às suas Organizations autorizadas.

O frontend nunca deve expor conceitos internos antigos como:

- Company;
- Site;
- vínculos diretos de Asset com Site.

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

- 005-multi-tenancy.md
- 006-api-refactor.md
- 007-data-migration.md

---

# Contexto Atual

O frontend atual foi desenvolvido considerando o domínio inicial.

Estrutura conceitual:

```text
Empresa

 ↓

Site

 ↓

Ativos

 ↓

Varreduras
```

---

# Problemas Identificados

A interface atual possui:

- nomenclatura divergente;
- componentes baseados em Site;
- consultas dependentes de endpoints antigos;
- ausência da hierarquia Project;
- baixa representação do conceito SaaS.

---

# Novo Modelo de Navegação

A experiência esperada:

```text
Dashboard

    |

Organizations

    |

Projects

    |

Assets

    |

Scans

    |

Findings

    |

Vulnerabilities
```

---

# Alterações de Navegação

## Antes

Menu:

```text
Dashboard

Empresas

Sites

Scans

Ameaças

Vulnerabilidades
```

---

## Depois

Menu:

```text
Dashboard

Organizações

Projetos

Ativos

Scans

Ameaças

Vulnerabilidades
```

---

# Componentes Impactados

## Organizations

Antes:

```text
Companies.jsx
```

Depois:

```text
Organizations.jsx
```

Responsabilidades:

- listar Organizations;
- criar;
- editar;
- visualizar contexto.

---

## Projects

Antes:

```text
Sites.jsx
```

Depois:

```text
Projects.jsx
```

Mudança conceitual:

O componente deixa de gerenciar websites.

Agora gerencia:

```text
Projetos de segurança
```

Exemplo:

```text
Projeto:
Portal Institucional

Ativos:

- Website
- API
- Subdomínio
```

---

## Assets

Atualizar:

```text
Assets.jsx
```

Novo comportamento:

Exibir:

```text
Project

 ↓

Assets
```

Informações:

- nome;
- tipo;
- valor;
- status;
- última análise.

---

## Scans

Atualizar:

```text
Scans.jsx
```

Fluxo:

Antes:

```text
Selecionar Site

Executar Scan
```

Depois:

```text
Selecionar Project

↓

Selecionar Asset

↓

Executar Scan
```

---

## Threat Management

Componentes:

```text
SignalsFindings.jsx

Vulnerabilities.jsx

Recommendations.jsx
```

Atualizar referências:

Antes:

```text
Site
```

Depois:

```text
Project

Asset
```

---

# API Client

Arquivo:

```text
api.js
```

Atualizar endpoints:

Antes:

```javascript
/companies

/sites
```

Depois:

```javascript
/organizations

/projects
```

---

# Modelos Frontend

Remover referências:

```javascript
company_id

site_id
```

Adicionar:

```javascript
organization_id

project_id

asset_id
```

---

# Estado Global

Caso exista gerenciamento global de contexto:

Atualizar:

Antes:

```text
Current Company
```

Depois:

```text
Current Organization
```

---

# Dashboard

Atualizar indicadores.

Antes:

```text
Quantidade de Sites

Quantidade de Scans
```

Depois:

```text
Organizations

Projects

Assets

Scans

Vulnerabilities
```

---

# Experiência SaaS

O frontend deverá preparar evolução futura para:

## Multi Organization

Usuário poderá futuramente possuir:

```text
Organization A

Organization B
```

com troca de contexto.

---

## Planos

Preparar componentes para:

```text
Assets utilizados

Scans executados

Limites do plano
```

---

## Permissões

Interface deve respeitar:

```text
Owner

Administrator

Analyst

Viewer
```

Exemplo:

Viewer:

```text
Sem botão de exclusão
```

---

# Segurança no Frontend

O frontend nunca deve ser a única camada de segurança.

Responsabilidades:

Frontend:

- esconder ações não permitidas;
- melhorar experiência.

Backend:

- validar autorização real.

---

# Estratégia de Implementação

Executar em etapas:

```text
1. Atualizar cliente API

        ↓

2. Atualizar navegação

        ↓

3. Renomear componentes

        ↓

4. Criar Projects UI

        ↓

5. Ajustar Assets

        ↓

6. Ajustar Scans

        ↓

7. Validar integração
```

---

# Compatibilidade Visual

Manter:

- tema escuro;
- identidade visual atual;
- responsividade;
- componentes existentes.

A migração deve alterar o modelo, não destruir a experiência criada.

---

# Testes Necessários

Validar:

## Organização

Usuário visualiza apenas Organizations autorizadas.

---

## Projeto

Criar:

```text
Project dentro de Organization
```

---

## Asset

Associar:

```text
Asset → Project
```

---

## Scan

Executar:

```text
Project + Asset
```

---

## Segurança

Usuário sem permissão:

```text
Botões ocultos

API bloqueada
```

---

# Critérios de Aceitação

A task será considerada concluída quando:

## Interface

- Não existir referência visual a Site;
- Organização substituir Empresa;
- Projeto substituir Site;
- Asset possuir contexto próprio.

---

## Integração

- Frontend consumir novos endpoints;
- Fluxos principais funcionando.

---

## Produto

A interface representar claramente:

```text
SaaS Security Platform
```

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
```

---

# Próximas Tasks Dependentes

Após conclusão:

```text
009-scan-engine-adaptation.md

↓

010-regression-tests.md
```

---

# Observação Final

O frontend é a camada onde o usuário percebe a evolução do Mouse IA.

A mudança de Company/Site para Organization/Project/Asset não é apenas uma alteração técnica.

É a transformação da percepção do produto:

De uma ferramenta de varredura.

Para uma plataforma SaaS de segurança.