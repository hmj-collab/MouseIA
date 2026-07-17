# Task: AI Engine & Recommendations (v0.4 - Epic 1 & 2)

## 1. Visão Geral
Esta tarefa visa implementar a inteligência artificial generativa no Mouse IA. Através da API do **Google Gemini**, a plataforma será enriquecida com a capacidade de analisar vulnerabilidades em profundidade e gerar explicações detalhadas, guias de correção personalizados e análises de probabilidade de falsos positivos.

Usaremos uma abordagem livre de dependências adicionais pesadas, integrando a chamada do Gemini diretamente via requisições HTTP (usando `httpx`) para a API oficial do Gemini.

---

## 2. Escopo Funcional

### A. AI Engine (Epic 1)
1. **Explicações Contextuais:** Converter saídas técnicas abstratas de scanners em descrições compreensíveis em linguagem natural (Português).
2. **Priorização e Impacto:** Explicar claramente qual o impacto para a empresa caso a vulnerabilidade seja explorada.

### B. Recommendations & Hardening (Epic 2)
1. **Guias de Correção:** Instruções passo a passo de como fechar a vulnerabilidade para diferentes tecnologias (Nginx, Apache, WordPress, etc.).
2. **Diretivas de Configuração:** Sugerir patches e linhas de configuração reais (ex: blocos de configuração do Nginx ou trechos de código PHP).

### C. False Positive Analysis (Epic 3)
1. **Classificação de Confiança:** Analisar as evidências técnicas capturadas pelo sinal para fornecer uma nota de confiança (Confidence Score) de 0% a 100%.
2. **Identificação de Falso Positivo:** Explicar se o sinal detectado pode ser um falso alarme devido a camuflagem de banners ou configurações parciais.

---

## 3. Estrutura do Endpoint do Gemini

Utilizaremos o modelo `gemini-1.5-flash` ou `gemini-2.5-flash` através da rota REST oficial:
```
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}
```

### Exemplo de Payload
```json
{
  "contents": [{
    "parts": [{
      "text": "Explique a vulnerabilidade CVE-2023-32243..."
    }]
  }],
  "generationConfig": {
    "responseMimeType": "application/json",
    "responseSchema": {
      "type": "OBJECT",
      "properties": {
        "explanation": {"type": "STRING"},
        "business_impact": {"type": "STRING"},
        "remediation_steps": {"type": "STRING"},
        "confidence_score": {"type": "INTEGER"},
        "is_false_positive": {"type": "BOOLEAN"},
        "false_positive_reason": {"type": "STRING"}
      },
      "required": ["explanation", "business_impact", "remediation_steps", "confidence_score", "is_false_positive"]
    }
  }
}
```

---

## 4. Plano de Implementação

1. **Configuração de Ambiente:**
   - Adicionar a variável de configuração `GEMINI_API_KEY` em `backend/app/core/config.py`.
2. **Serviço Central `AIService`:**
   - Criar `backend/app/services/ai_service.py` contendo os métodos:
     - `analyze_vulnerability(self, vuln: Vulnerability) -> dict`
3. **Controlador e API Endpoints:**
   - Criar endpoint `POST /vulnerabilities/{id}/ai-analysis` para disparar a análise de inteligência sob demanda.
4. **Atualização da Interface (Frontend):**
   - Adicionar uma aba "Análise de IA" nos detalhes de Vulnerabilidades exibindo o impacto executivo, justificativa técnica e guias práticos de correção estruturados de forma atraente.
5. **Testes Automatizados:**
   - Criar suíte de testes simulando requisições com mocks HTTP para garantir o comportamento do serviço sob falhas de rede ou indisponibilidade de chave de API.
