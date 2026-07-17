# Manual Completo do Usuário e do Desenvolvedor (Mouse IA)

Bem-vindo ao manual oficial de documentação do **Mouse IA**, a plataforma profissional de **Attack Surface Management (ASM)**, **Threat Intelligence** e **AI Security Analytics**.

Esta documentação foi elaborada para servir como referência completa para usuários finais, auditores de segurança e desenvolvedores que trabalham na evolução do ecossistema.

---

## 📖 Índice de Capítulos

Selecione um capítulo abaixo para navegar pela documentação detalhada:

### [Capítulo 1: Introdução e Arquitetura](file:///Users/hmjfotografia/MouseIA/docs/manual/01-introducao.md)
* Visão geral da plataforma
* Tecnologias e bibliotecas utilizadas
* Padrões de arquitetura e fluxo de dados (Clean Architecture)

### [Capítulo 2: Guia de Instalação e Configuração](file:///Users/hmjfotografia/MouseIA/docs/manual/02-instalacao.md)
* Requisitos mínimos do sistema
* Instalação passo a passo (Backend, Banco de dados SQLite/PostgreSQL, Frontend)
* Variáveis de Ambiente e chaves de API (Gemini, etc.)
* Execução e validação da suíte de testes (`pytest`)

### [Capítulo 3: Guia de Funcionalidades e Operação](file:///Users/hmjfotografia/MouseIA/docs/manual/03-funcionalidades.md)
* Controle de Acesso e Autenticação (RBAC)
* Gestão de Escopo (Organizações, Projetos e URLs de Destino)
* Execução de Varreduras (Scans ativos de rede, auditoria de headers e detecção WordPress)
* Fluxo de Sinais e Correlação (Correlation Engine)

### [Capítulo 4: Inteligência Artificial e Falsos Positivos](file:///Users/hmjfotografia/MouseIA/docs/manual/04-inteligencia-artificial.md)
* Motor de IA (Gemini API Integration)
* Relatórios estruturados de IA em tempo de execução
* Mitigação e filtragem automática de Falsos Positivos durante a ingestão
* Penalização de Risk Score por IA

### [Capítulo 5: Governança, Métricas e Exportações](file:///Users/hmjfotografia/MouseIA/docs/manual/05-relatorios-e-exportacoes.md)
* Dashboard de Governança (Cálculos de SLA e MTTR)
* Exportação técnica de dados em formato CSV
* Emissão e Salvamento de Relatórios Executivos em PDF
