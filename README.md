# Mouse IA

Mouse IA é uma plataforma profissional de gestão inteligente de vulnerabilidades e superfícies de ataque. A proposta do projeto vai além de um simples scanner de WordPress e evolui para uma solução modular para análise contínua de segurança.

O projeto está estruturado para começar com o módulo de Sites e, no futuro, expandir para integrações com GitHub, Azure DevOps, GitLab, Docker, Kubernetes, Nginx, Apache, IIS, Linux, Windows, Cloudflare, SSL e DNS.

## Visão geral

Mouse IA foi idealizado para ajudar equipes de segurança a:

- cadastrar e gerenciar ativos digitais
- coletar sinais e evidências de segurança
- correlacionar informações e identificar riscos
- gerar achados, vulnerabilidades e recomendações
- organizar ações de remediação e acompanhamento

O fluxo central da plataforma é:

Asset → Scan → Signals → Correlation Engine → Findings → Vulnerabilities → Recommendations → Tasks

## Status do projeto

O projeto encontra-se em fase inicial de estruturação. A base arquitetural, os diretórios principais e a documentação de referência já foram organizados, com foco no desenvolvimento de uma plataforma escalável e modular.

## Arquitetura e organização

A solução foi pensada em camadas e módulos, com separação clara entre:

- Backend: APIs, regras de negócio, serviços e integração com dados
- Frontend: interface para navegação, gestão e visualização
- Documentação: arquitetura, roadmap, segurança e contexto do produto
- Infraestrutura: suporte para banco de dados, filas, cache e execução em containers

## Estrutura do repositório

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── domain/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── scanners/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── workers/
│   │   └── main.py
│   ├── alembic/
│   ├── intel/
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── services/
│   └── types/
├── docker/
├── docs/
├── scripts/
├── ARCHITECTURE.md
├── ROADMAP.md
├── SECURITY.md
├── SIGNALS.md
└── CHANGELOG.md
```

## Principais módulos previstos

### Módulo de Sites

Responsável por cadastrar sites para auditoria, com atributos como nome, URL, ambiente, empresa, categoria, tecnologia, status, data de criação, último scan e score atual.

### Módulos futuros

- Empresas
- Ativos
- Scans
- Sinais
- Findings
- Vulnerabilidades
- Recomendações
- Tarefas
- Integrações com ecossistemas externos

## Tecnologias e pilares de desenvolvimento

O projeto foi pensado com foco em:

- Python 3.x com FastAPI
- PostgreSQL como base principal
- Alembic para versionamento de schemas
- arquitetura modular e escalável
- uso de filas para processamento assíncrono
- uso de cache para otimização de leitura
- integração com inteligência artificial como camada de apoio
- atualização contínua de bases como CVE, NVD, CISA KEV e EPSS

## Como começar

1. Clone o repositório.
2. Configure as variáveis de ambiente com base no arquivo .env.example.
3. Estruture o ambiente backend e frontend conforme a evolução do projeto.
4. Consulte a documentação de arquitetura e roadmap para acompanhar a direção da plataforma.

## Documentação relacionada

- [ARCHITECTURE.md](ARCHITECTURE.md): visão técnica e arquitetura da solução
- [ROADMAP.md](ROADMAP.md): evolução do projeto por fases
- [SECURITY.md](SECURITY.md): diretrizes de segurança
- [SIGNALS.md](SIGNALS.md): fluxo conceitual de sinais e análise
- [CHANGELOG.md](CHANGELOG.md): histórico de mudanças

## Próximos passos

As próximas etapas previstas incluem:

- implementação do módulo inicial de Sites
- definição dos modelos e APIs base
- evolução para o fluxo completo de scan, sinais e findings
- integração com frontend e infraestrutura operacional

## Licença

Este projeto está sob a licença definida no arquivo LICENSE.
