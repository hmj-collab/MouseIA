# Task: Automated False Positive Detection & Ingestion Enrichment (v0.4 - Epic 3)

## 1. Visão Geral
Durante a ingestão e correlação de novos achados, queremos analisar se a detecção técnica gerada pelo scan tem alta probabilidade de ser um falso positivo. Para isso, o **Correlation Engine** invocará o **AIService** em segundo plano durante a criação das vulnerabilidades para:
- Detectar se a evidência reportada pelo sinal sugere um falso positivo.
- Ajustar dinamicamente o `risk_score` da vulnerabilidade caso ela seja considerada um falso positivo (multiplicador de 0.1).
- Atualizar a descrição da vulnerabilidade para anexar a explicação contextual gerada pela IA de forma imediata.

---

## 2. Fluxo de Execução Unificado

```
1. Scan Conclui
       │
       ▼
2. process_new_signals()
       │
       ▼
3. correlate_finding() (Gera Vulnerabilidade)
       │
       ▼
4. Enriquecimento de IA (Ocorre no correlate_finding)
   - Executa AIService.analyze_vulnerability()
   - Se is_false_positive == True:
     - Define status = "mitigated" (ou mantém aberto mas com flag)
     - Aplica multiplicador 0.1 no risk_score (ex: 8.9 -> 0.89)
   - Adiciona a explicação da IA no final da descrição.
```

---

## 3. Plano de Implementação

1. **Atualização do `CorrelationService`:**
   - Adicionar uma chamada automática ao `AIService` ao criar novas vulnerabilidades em `correlate_finding()`.
   - Modificar a fórmula do `risk_score` para reduzir em 90% (multiplicador de 0.1) se `is_false_positive` for True.
   - Anexar as explicações da IA diretamente à descrição técnica da vulnerabilidade.
2. **Atualização da Interface (Frontend):**
   - Garantir que a nota de confiança e o status de Falso Positivo analisado pela IA já venham pré-exibidos sem a necessidade de clicar em um botão sob demanda (enriquecimento na ingestão).
3. **Testes de Integração:**
   - Adicionar casos de testes validando se vulnerabilidades marcadas como falso positivo pela IA têm suas notas de risco ajustadas para perto de 0 automaticamente.
