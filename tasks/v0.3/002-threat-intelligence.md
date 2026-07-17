# Task: Threat Intelligence & Risk Score (v0.3 - Epic 2 & 3)

## 1. Visão Geral
O objetivo desta tarefa é dotar o Mouse IA de inteligência contextual sobre vulnerabilidades externas. Em vez de depender apenas de dados estáticos do scanner, a plataforma enriquecerá cada vulnerabilidade encontrada correlacionando-a com dados em tempo real (ou cacheados) de ameaças reais:
- **NVD (National Vulnerability Database):** Para dados oficiais de CVSS (Common Vulnerability Scoring System).
- **CISA KEV (Known Exploited Vulnerabilities):** Para identificar se a vulnerabilidade está sendo explorada ativamente no "mundo real".
- **EPSS (Exploit Prediction Scoring System):** Para obter a probabilidade estatística de a vulnerabilidade ser explorada nos próximos 30 dias.

Além disso, uniremos esses dados com a prioridade/criticidade do **Ativo Técnico** para calcular um **Risk Score Dinâmico**.

---

## 2. Arquitetura do Componente
Devido a limitações de limites de taxa (rate limiting), latência de rede e requisitos de execução offline/testes, o componente de Threat Intelligence funcionará sob um modelo de cache local:

```
                  ┌────────────────────────┐
                  │      Scan Engine       │
                  └───────────┬────────────┘
                              │ (sinais)
                              ▼
                  ┌────────────────────────┐
                  │   Correlation Engine   │
                  └───────────┬────────────┘
                              │ (findings)
                              ▼
                  ┌────────────────────────┐
                  │    Threat Intel        │
                  │   Enrichment Service   │
                  └──────┬──────────┬──────┘
                         │          │
        (se no cache)   │          │ (se não)
                         ▼          ▼
            ┌───────────────┐   ┌────────────────────────────────┐
            │ Cache Local   │   │ Clientes de API Externas       │
            │ (SQLite DB)   │   │ - FIRST EPSS API               │
            │               │   │ - CISA KEV JSON                │
            │               │   │ - NVD API / WordPress Advis    │
            └───────────────┘   └────────────────┬───────────────┘
                                                 │
                                                 ▼ (Salva no cache)
```

---

## 3. Modelo de Banco de Dados (`cve_intelligence`)
Para cachear as informações e garantir performance, criaremos uma tabela `cve_intelligence`:

```python
class CveIntelligence(Base, TimestampMixin):
    __tablename__ = "cve_intelligence"

    cve_id = Column(String(40), primary_key=True, index=True)
    cvss_score = Column(Float, nullable=True)
    severity = Column(String(40), nullable=True)  # critical, high, medium, low
    epss_score = Column(Float, nullable=True)       # valor entre 0.0 e 1.0 (probabilidade)
    is_kev = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    last_fetched_at = Column(DateTime(timezone=True), nullable=False)
```

---

## 4. Cálculo do Risk Score Personalizado (Epic 3)
O Risk Score de uma vulnerabilidade será um valor de **0.0 a 10.0** calculado com base na fórmula ponderada:

$$RiskScore = (CVSS \times 0.5) + (EPSS \times 10 \times 0.2) + (KEVMul \times 0.2) + (AssetWeight \times 0.1)$$

Onde:
- **CVSS:** Pontuação base (ex: 8.8). Se indisponível, assume severidade média (5.0).
- **EPSS:** Probabilidade (ex: 0.85 = 8.5 pontos).
- **KEVMul:** Se `is_kev` for True, soma **10.0** pontos. Se False, **0.0**.
- **AssetWeight:** Fator de criticidade do projeto/ativo (ex: Produção = 10.0, Homologação = 5.0, Teste = 1.0).

---

## 5. Plano de Implementação
1. **Modelagem & Migração:**
   - Criar modelo `CveIntelligence` em `backend/app/models/cve_intelligence.py`.
   - Adicionar chave estrangeira/relação nas tabelas de vulnerabilidades para integrar com o cache de inteligência.
   - Gerar e aplicar a migração correspondente.
2. **Desenvolvimento dos Clientes de API:**
   - Criar `backend/app/scanners/threat_intel/cisa_client.py` (Parser para o catálogo KEV da CISA).
   - Criar `backend/app/scanners/threat_intel/epss_client.py` (Busca da pontuação de exploração via API FIRST).
3. **Serviço Centralizado de Enriquecimento:**
   - Desenvolver o `ThreatIntelService` para coordenar buscas (usando cache local primeiro e fazendo requisição apenas se expirado ou não existente).
4. **Atualização da API & UI:**
   - Exibir no frontend as métricas de ameaças em tempo real (EPSS e status KEV) na visualização de detalhes de Vulnerabilidades.
5. **Testes Automatizados:**
   - Desenvolver testes integrados cobrindo simulação de respostas de API e checagem de regras de cálculo de score.
