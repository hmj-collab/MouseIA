# Fluxo de Signals do Mouse IA

## Visão geral

O Mouse IA organiza sua análise em um pipeline de sinais e evidências que transforma dados brutos em achados estruturados, vulnerabilidades contextualizadas e recomendações acionáveis.

O fluxo principal da plataforma segue a seguinte cadeia de processamento:

Asset → Scan → Signals → Correlation Engine → Findings → Vulnerabilities → Recommendations → Tasks

## 1. Asset

Representa o ativo digital ou elemento de infraestrutura alvo da análise.

### Exemplos técnicos
- sites
- repositórios
- servidores
- endpoints
- containers
- ambientes cloud

### Entrada
- identificador do ativo
- metadados operacionais
- contexto empresarial e técnico

### Saída
- objeto de análise com escopo definido
- contexto necessário para execução do scan

## 2. Scan

É a etapa de coleta e observação do estado do ativo.

### Tipos de coleta
- varreduras automáticas
- inspeção de configuração
- checagem de versões e componentes
- rastreamento de exposições e anomalias

### Entrada
- asset_id
- configuração do scan
- regras ou policies de coleta

### Saída
- conjunto de dados brutos
- evidências primárias
- metadados de execução

## 3. Signals

São os sinais observados a partir dos dados coletados.

### Exemplos técnicos
- versão desatualizada
- configuração insegura
- endpoint exposto
- erro de autenticação
- plugin vulnerável
- componente descontinuado
- comportamento anômalo

### Estrutura conceitual
- source: origem do sinal
- type: categoria do sinal
- severity: gravidade estimada
- confidence: confiança da observação
- timestamp: momento da detecção

### Implementação atual

O módulo já permite criar e consultar sinais pela API. O registro persistido contém `source`, `signal_type`, `severity`, `confidence`, `description` e um `site_id` opcional. As rotas de leitura exigem autenticação dos papéis `admin` ou `viewer`; a criação exige `admin`.

### Saída
- eventos analisáveis
- insumos para normalização e correlação

## 4. Correlation Engine

É o componente responsável por relacionar sinais, contexto e histórico para gerar uma visão mais rica e precisa.

### Funções principais
- reduzir ruído
- agrupar sinais semelhantes
- associar contexto operacional e empresarial
- enriquecer dados com fontes externas
- inferir padrões relevantes

### Fontes de contexto
- tecnologia do ativo
- ambiente onde ele está implantado
- criticidade da organização
- histórico de ocorrências anteriores
- bases externas como CVE, NVD, CISA KEV e EPSS

### Saída
- sinais enriquecidos
- hipóteses de risco
- contexto estruturado para geração de findings

## 5. Findings

São os achados estruturados gerados a partir dos sinais correlacionados.

### Características
- representam um problema ou risco identificável
- podem ser técnicos, operacionais ou de conformidade
- servem como unidade mínima de análise para o restante do pipeline

### Exemplo de estrutura
- title
- description
- severity
- evidence
- related_signals
- status

### Implementação atual

O módulo já permite criar e consultar findings pela API. O registro persistido contém `title`, `description`, `severity`, `status` e um `signal_id` opcional. A geração automática a partir da correlação de sinais ainda não foi implementada.

### Saída
- achados normalizados
- evidência consolidada para análise posterior

## 6. Vulnerabilities

São as vulnerabilidades associadas aos findings, com contexto técnico e de risco.

### Conteúdo esperado
- identificadores de vulnerabilidades conhecidas
- referências a CVE/NVD
- classificação de severidade
- impacto potencial
- recomendação técnica preliminar

### Objetivo
- contextualizar o problema com base em conhecimento externo
- apoiar priorização e resposta baseada em risco

## 7. Recommendations

São as recomendações geradas para mitigar os riscos identificados.

### Exemplos técnicos
- atualizar software ou biblioteca
- restringir exposição de serviços
- corrigir configuração insegura
- bloquear acesso indevido
- reconfigurar autenticação e segredos

### Objetivo
- converter achados em ações remediativas
- oferecer orientação objetiva para mitigação

## 8. Tasks

São as tarefas operacionais derivadas das recomendações.

### Campos comuns
- title
- description
- assignee
- priority
- status
- due_date
- related_recommendation

### Objetivo
- transformar recomendações em execução prática
- garantir rastreabilidade e acompanhamento

## 9. Fluxo técnico resumido

O pipeline do Mouse IA pode ser descrito em etapas operacionais:

1. identificar e registrar um ativo
2. executar uma coleta via scan
3. extrair sinais relevantes
4. normalizar e correlacionar sinais com contexto
5. gerar findings
6. associar vulnerabilidades conhecidas
7. produzir recomendações de mitigação
8. converter em tarefas executáveis

## 10. Valor técnico do pipeline

Esse pipeline permite que a plataforma:

- organize dados de forma estruturada e rastreável
- aumente a precisão da análise
- priorize riscos com maior contexto
- transforme observações técnicas em ações operacionais
- facilite integração com módulos futuros e fontes externas

## 11. Estado atual e próximos passos

Sites, Signals e Findings já possuem persistência e endpoints protegidos. Ainda faltam o módulo de Scan, a coleta automatizada, a correlação, o enriquecimento externo e os módulos de Vulnerabilities, Recommendations e Tasks. O pipeline será expandido mantendo esta arquitetura de processamento e normalização.
