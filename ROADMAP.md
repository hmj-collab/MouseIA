# Roadmap do Mouse IA

Este documento organiza a evolução do projeto em fases, com foco em construir uma plataforma modular, escalável e orientada a análise contínua de segurança.

## Status atual

A base técnica já está funcional localmente:

- estrutura do backend consolidada
- módulo de Sites operando com CRUD protegido
- módulos de Signals e Findings com criação e consulta protegidas
- persistência com SQLAlchemy e Alembic
- autenticação JWT e autorização por papéis
- interface estática local de teste
- testes automatizados em execução para os módulos implementados

## Fase 0 - Fundação (concluída parcialmente)
Objetivo: estruturar a base técnica e conceitual do projeto.

- estrutura inicial do repositório concluída
- documentação central organizada
- arquitetura inicial definida
- base de backend implementada
- padrões de testes e migrações incorporados

## Fase 1 - Núcleo da plataforma (em andamento)
Objetivo: disponibilizar os blocos centrais para uso e operação.

- criar gestão de usuários e empresas
- estruturar um dashboard inicial
- consolidar a experiência de navegação do frontend além da interface de teste atual

## Fase 2 - Coleta e varredura
Objetivo: incorporar os primeiros mecanismos de ingestão e análise.

- desenvolver o fluxo de scan e coleta automatizada de sinais
- integrar fontes de dados e ativos relevantes
- estruturar o processamento inicial de evidências
- evoluir o CRUD de Signals e Findings com atualização, exclusão e filtros

## Fase 3 - Inteligência e correlação
Objetivo: transformar sinais brutos em contexto útil.

- implementar o motor de correlação de sinais
- criar a lógica de identificação de vulnerabilidades
- organizar a correlação automática de findings e priorização de riscos
- definir regras de análise e contexto operacional

## Fase 4 - IA e recomendações
Objetivo: ampliar a plataforma com suporte inteligente.

- integrar recursos de IA para análise e resumo
- gerar recomendações baseadas em achados
- apoiar a priorização de ações e triagem
- melhorar a experiência do usuário com automação assistida

## Fase 5 - Relatórios e governança
Objetivo: tornar a plataforma útil para acompanhamento e decisão.

- criar relatórios claros e estruturados
- implementar histórico de eventos e mudanças
- organizar configurações e preferências do sistema
- adicionar rastreabilidade e auditoria

## Fase 6 - Escala e integração
Objetivo: preparar a plataforma para ambiente real e uso contínuo.

- documentar a API e os fluxos de integração
- melhorar a segurança, observabilidade e deploy
- preparar a plataforma para ambientes containerizados
- expandir integrações externas e automações

## Critérios de sucesso

A evolução do projeto será considerada bem-sucedida quando:

- a estrutura principal estiver funcional localmente
- o fluxo Asset → Scan → Signals → Findings estiver operacional
- o usuário conseguir navegar, consultar e acompanhar resultados
- a documentação estiver suficiente para onboarding e evolução técnica

## Status geral

O projeto está em uma fase inicial, porém já possui autenticação e autorização, persistência e os primeiros elementos do pipeline operacional: Sites, Signals e Findings.
