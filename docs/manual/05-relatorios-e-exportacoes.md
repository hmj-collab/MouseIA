# Capítulo 5: Governança, Métricas e Exportações

Este capítulo apresenta o funcionamento dos painéis gerenciais (Dashboards), os cálculos de conformidade técnica e o fluxo para exportação de dados e relatórios em PDF.

---

## 1. Dashboard de Governança e Métricas
O Dashboard consolidado fornece métricas avançadas sobre a postura de conformidade da infraestrutura monitorada.

### Risk Score Médio
O Risk Score Médio representa a média aritmética dos risk scores calculados para todas as vulnerabilidades que permanecem com status `"open"` (em aberto). Ele dá um termômetro em tempo real do nível de exposição de ativos.

### Tempo Médio de Resposta (MTTR)
O **MTTR (Mean Time to Remediation)** indica a média de tempo gasta para mitigar ou resolver vulnerabilidades detectadas.
* **Cálculo:** O backend calcula a diferença de tempo (em horas) entre o momento de criação da vulnerabilidade (`created_at`) e a data em que o seu status foi atualizado para `"resolved"` ou `"mitigated"` (`updated_at`).
* **Fórmula:**
  $$\text{MTTR} = \frac{\sum (\text{updated\_at} - \text{created\_at})}{\text{Quantidade de Vulnerabilidades Resolvidas}}$$

### Conformidade com SLA (Service Level Agreement)
A conformidade com SLA é calculada como o percentual de vulnerabilidades corrigidas dentro do prazo aceitável padrão de mercado de acordo com sua criticidade técnica:
* **Severidade Crítica (`critical`):** SLA de **7 dias** (168h).
* **Severidade Alta (`high`):** SLA de **15 dias** (360h).
* **Severidade Média (`medium`):** SLA de **30 dias** (720h).
* **Severidade Baixa / Info (`low` / `info`):** SLA de **90 dias** (2160h).

* **Fórmula:**
  $$\text{SLA Compliance \%} = \left( \frac{\text{Vulnerabilidades Resolvidas dentro do SLA}}{\text{Total de Vulnerabilidades Resolvidas}} \right) \times 100$$

---

## 2. Exportação de Dados em CSV
Para permitir que analistas técnicos manipulem os inventários de vulnerabilidade e gerem planilhas no Excel, a plataforma expõe funcionalidades de exportação direta:
* **Botão "Exportar CSV"** na tela de Análise e Mitigação.
* **Colunas Exportadas:** ID da Vulnerabilidade, CVE ID, Título, Descrição Técnica, Severidade, CVSS Score, Risk Score de IA, Status atual (Aberto/Mitigado/Aceito/Resolvido), ID do Ativo e Data de Criação.

---

## 3. Emissão de Relatório Executivo em PDF
A geração de relatórios de conformidade para auditoria é efetuada através do botão **"Imprimir PDF"** na tela de Análise e Mitigação.

### Como Funciona:
Ao clicar em "Imprimir PDF", o sistema executa o método `window.print()` do navegador. O arquivo global de estilos ([index.css](file:///Users/hmjfotografia/MouseIA/frontend/src/index.css)) possui instruções dedicadas de impressão (`@media print`):
1. **Ocultação de Elementos de Interface:** Menus de navegação, cabeçalhos, botões, caixas de filtro e formulários de input são automaticamente ocultados da página.
2. **Formatação de Alto Contraste:** O fundo escuro (dark mode) da plataforma é convertido em um fundo branco de papel e as fontes escuras de alto contraste são aplicadas, economizando tinta de impressão e otimizando a leitura.
3. **Quebra de Página Automatizada:** A listagem e os cartões de vulnerabilidade são otimizados com `page-break-inside: avoid` para evitar que uma vulnerabilidade seja cortada ao meio na divisão de páginas do PDF.

*Isso permite gerar um relatório gerencial impresso ou salvo em PDF em um clique, de forma rápida, leve e sem necessidade de processamento demorado no backend.*
