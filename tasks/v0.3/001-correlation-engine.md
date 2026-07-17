# Task: Correlation Engine (v0.3 - Epic 1)

## 1. Visão Geral
O **Correlation Engine** é o cérebro analítico do Mouse IA. Ele é responsável por processar os sinais de segurança brutos (`Signals`) gerados pelos Scans e correlacioná-los em problemas consolidados de segurança (`Findings`).

Atualmente, a plataforma cria um `Finding` para cada `Signal` gerado, gerando muito ruído e duplicação. O objetivo deste motor é:
1. **Reduzir Ruído:** Agrupar múltiplos sinais relacionados de uma mesma execução de scan sob um único `Finding`.
2. **Deduplicação Temporal:** Se um sinal idêntico for gerado em um scan subsequente para o mesmo ativo, associá-lo ao `Finding` já aberto (atualizando sua evidência/data de atualização) em vez de criar um novo registro duplicado.
3. **Mapeamento:** Associar adequadamente os achados a vulnerabilidades conocidas (CVE) e recomendações.

---

## 2. Alterações de Modelo de Dados
Para suportar o agrupamento de múltiplos sinais em um único Finding, o relacionamento atual 1-para-1 invertido (`Finding.signal_id`) deve ser evoluído.

### Proposta de Schema:
1. **Model `Signal` (`backend/app/models/signal.py`):**
   - Adicionar uma chave estrangeira opcional `finding_id` relacionando a `findings.id`.
   - Adicionar o relacionamento ORM correspondente.
2. **Model `Finding` (`backend/app/models/finding.py`):**
   - Manter ou remover gradualmente o campo `signal_id` legando a associação primária para o lado do `Signal` (`Signal.finding_id`). Isso permite uma relação 1-para-M (um Finding possui múltiplos Signals).

---

## 3. Regras de Correlação & Agrupamento
Implementaremos as seguintes regras no `CorrelationService`:

### A. Lógica de Deduplicação
Antes de criar um novo `Finding` para um `Signal` recebido em um `Asset`:
- Consultar se existe algum `Finding` com `status == "open"` associado a um sinal do mesmo `signal_type` para o mesmo `asset_id`.
- **Se existir:** Vincular o novo `Signal` a este `Finding` existente, atualizar a data de modificação e anexar a descrição do novo sinal ao histórico de evidências do Finding.
- **Se não existir:** Criar um novo `Finding` e vincular o sinal a ele.

### B. Regras de Agrupamento por Categoria (Grouping Rules)
Sinais de tipos diferentes mas que partilham da mesma raiz de problema devem ser consolidados no mesmo `Finding`.
- **Grupo 1: "Configuração Insegura de Cabeçalhos HTTP"**
  - Sinais: `missing_csp`, `missing_hsts`, `missing_x_frame_options`, `leak_server`, `leak_x_powered_by`.
- **Grupo 2: "Exposição de Infraestrutura WordPress"**
  - Sinais: `wordpress_detected`, `wp_login_exposed`, `xmlrpc_enabled`, `wp_directory_listing`.

---

## 4. Plano de Implementação
1. **Migração de Banco de Dados:** Criar uma migração Alembic para adicionar `finding_id` na tabela `signals`.
2. **Atualização dos Schemas:** Atualizar schemas Pydantic de `Signal` para incluir `finding_id`.
3. **Refatoração do `CorrelationService`:**
   - Reescrever o método de processamento de sinais para aplicar as regras de deduplicação e agrupamento.
   - Atualizar a criação de `Vulnerability` e `Recommendation` a partir do `Finding` consolidado.
4. **Testes Automatizados:**
   - Adicionar testes de unidade no `backend/tests/` validando cenários de deduplicação e agrupamento de sinais.
