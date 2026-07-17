# Task: Reporting, Dashboards & Export (v0.5 - Epic 1, 2, 3 & 4)

## 1. Visão Geral
Esta tarefa visa implementar as ferramentas de relatórios, métricas gerenciais e exportação de dados no Mouse IA. Permitiremos que gestores (nível executivo) e analistas (nível técnico) acompanhem a evolução da segurança, exportem dados técnicos de vulnerabilidades para planilhas e gerem relatórios consolidados em PDF.

---

## 2. Escopo Funcional

### A. Dashboard Executivo & Técnico (Epic 1 & 2)
1. **Métricas de KPI:**
   - **Média de Risk Score:** Exposição média dos ativos da empresa.
   - **MTTR (Mean Time to Remediation):** Tempo médio gasto para fechar uma vulnerabilidade.
   - **SLA de Correção:** % de vulnerabilidades corrigidas dentro do prazo aceitável (Crítica: 7 dias, Alta: 15 dias, Média: 30 dias).
2. **Distribuição Temporal (Vulnerabilidades Criadas vs Corrigidas):**
   - Gráfico de tendências (últimos 30 dias).

### B. Exportações de Dados (Epic 4)
1. **Botões de Download (CSV / JSON):**
   - Disponibilizar na tela de Vulnerabilidades e no Dashboard a opção de exportar o inventário filtrado diretamente como planilhas CSV ou arquivos JSON estruturados.

### C. Relatórios em PDF (Epic 3)
1. **Template de Relatório Gerencial:**
   - Desenvolver um endpoint backend ou uma folha de estilo CSS para impressão (`@media print`) que formate a página de Vulnerabilidades em um layout de relatório de auditoria limpo, profissional, colorido e sem barras de navegação (ideal para salvar como PDF diretamente do navegador com Ctrl+P/Cmd+P).

---

## 3. Plano de Implementação

1. **Backend - Relação de Métricas:**
   - Criar endpoint `GET /dashboard/metrics` em `backend/app/api/dashboard.py` (ou atualizar controllers) fornecendo:
     - MTTR (calculado pela diferença entre `created_at` e `updated_at` de vulnerabilidades com status `resolved` ou `mitigated`).
     - Distribuição de risco consolidada.
2. **Backend - Geração de Relatórios e Exportação:**
   - Criar endpoint `GET /vulnerabilities/export` retornando payload formatado em CSV.
3. **Frontend - Visualização Gráfica:**
   - Refatorar o [Dashboard.jsx](file:///Users/hmjfotografia/MouseIA/frontend/src/components/Dashboard.jsx) para exibir as novas métricas de SLA e MTTR.
   - Implementar os botões de exportação (CSV/JSON).
4. **Folha de Impressão PDF:**
   - Adicionar estilos `@media print` no CSS global ou no componente para formatar a página de relatório em um layout executivo em formato PDF.
5. **Testes Automatizados:**
   - Criar testes integrados para o endpoint de métricas e exportação CSV.
