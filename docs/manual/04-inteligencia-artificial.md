# Capítulo 4: Inteligência Artificial e Falsos Positivos

Este capítulo descreve a integração da Inteligência Artificial (Google Gemini) na plataforma, abordando a triagem de vulnerabilidades, geração de guias de hardening e a redução inteligente de falsos positivos.

---

## 1. Integração com a API do Google Gemini
O Mouse IA utiliza o modelo de linguagem **Gemini 1.5 Flash** para analisar as evidências de vulnerabilidades ingeridas de forma contextual.

### Arquitetura de Requisição:
* **Conexão Direta:** As requisições são efetuadas diretamente utilizando chamadas HTTP assíncronas via biblioteca `httpx` para o endpoint oficial `generateContent` do Gemini. Isso evita dependências externas complexas de SDKs e otimiza o tempo de resposta.
* **JSON Schema Restrito:** A chamada envia instruções detalhadas e impõe um esquema de resposta estruturado (`responseSchema`) em JSON. O modelo retorna estritamente os campos mapeados na estrutura do sistema, garantindo previsibilidade total.

---

## 2. Relatórios Estruturados de IA
A IA enriquece a vulnerabilidade gerando as seguintes seções de relatório:
* **Explicação Executiva:** Tradução do termo técnico da falha em linguagem comercial simples e acessível para tomadores de decisão.
* **Impacto Comercial (Business Impact):** Consequências financeiras ou operacionais caso a falha seja explorada (ex: vazamento de dados, injeção XSS, indisponibilidade do serviço).
* **Guia de Hardening (Remediação):** Lista ordenada passo a passo com comandos de código específicos e alterações de configuração (para Nginx, Apache ou código-fonte) para sanar o problema.
* **Score de Confiança:** Um valor numérico de 1 a 100 indicando o grau de certeza da inteligência na detecção efetuada.

---

## 3. Identificação e Mitigação Automática de Falsos Positivos
Durante a ingestão das varreduras através do **Correlation Engine**, o sistema submete a vulnerabilidade recém-criada à análise automática do `AIService` para validar se as evidências do scan indicam um falso positivo.

```
       [ Scan Concluído ]
               │
               ▼
   [ Criação da Vulnerabilidade ]
               │
               ▼
   [ Execução do AIService ]
               │
      Is False Positive?
         /           \
       SIM           NÃO
       /               \
 - Status = "mitigated"   - Status = "open"
 - Risk Score * 0.1       - Risk Score Padrão
 - Nota de Falso Positivo
```

* **Mitigação Automática:** Se o modelo de IA determinar que a ameaça é um falso positivo (ex: um componente simulado de teste ou assinatura incompatível), o `status` da vulnerabilidade é automaticamente alterado de `"open"` (aberto) para `"mitigated"` (mitigado).
* **Penalização do Risk Score (Multiplicador de 0.1):** Vulnerabilidades identificadas como falso positivo têm seu Risk Score multiplicado por `0.1` (redução de 90%). Por exemplo, um risco Crítico com pontuação de `9.0` cai para `0.9` (Baixo). Isso impede que falsos positivos poluam a visão gerencial do Dashboard e a triagem prioritária.
* **Adição de Aviso de Falso Positivo:** A justificativa e evidências analisadas pela IA são indexadas no final do campo de descrição técnica da vulnerabilidade, provendo rastreabilidade para o analista.
