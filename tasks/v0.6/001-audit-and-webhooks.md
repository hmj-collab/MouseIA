# Task: Audit Logging & Webhooks Integration (v0.6 - Epic 3 & 5)

## 1. Visão Geral
Para habilitar a conformidade empresarial, implementaremos uma **Trilha de Auditoria (Audit Logs)** e um motor de **Webhooks de Integração**. Isso dará transparência total sobre as atividades dos usuários do sistema e permitirá alertar sistemas externos (SIEM, Slack, Microsoft Teams, Discord) em tempo real sobre novas vulnerabilidades de alto risco encontradas.

---

## 2. Escopo Técnico

### A. Trilha de Auditoria (Epic 3)
1. **Modelagem de Banco de Dados (`audit_logs`):**
   * `id`: Chave primária.
   * `user_id`: ID do usuário que executou a ação.
   * `action`: Descritor da ação executada (ex: `LOGIN`, `CREATE_PROJECT`, `LAUNCH_SCAN`, `MITIGATE_VULNERABILITY`).
   * `target_type`: Tipo do recurso afetado (ex: `project`, `scan`, `vulnerability`, `user`).
   * `target_id`: ID do recurso afetado.
   * `details`: JSON ou string com detalhes da alteração (valores antigos vs novos se aplicável).
   * `timestamp`: Data e hora em UTC.
2. **Serviço de Auditoria (`AuditService`):**
   * Helper unificado para fácil inserção de logs de auditoria a partir dos controllers.
3. **API e Visualização:**
   * Endpoint `GET /audit-logs` com paginação e filtro por usuário.
   * Exposição na interface web em uma nova aba dedicada de Configurações ou Segurança (visível apenas para administradores).

### B. Motor de Webhooks (Epic 5)
1. **Modelagem de Banco de Dados (`webhooks`):**
   * `id`: Chave primária.
   * `name`: Nome identificador da integração.
   * `url`: Endpoint HTTP de destino (URL do Webhook).
   * `secret_token`: Token para assinatura criptográfica do payload (evita falsificação).
   * `is_active`: Controle de ativação.
   * `trigger_events`: Lista de eventos que disparam o webhook (ex: `scan_completed`, `critical_vuln_found`).
2. **Serviço de Disparo (`WebhookService`):**
   * Executa requisições HTTP POST em background enviando payloads JSON contendo os detalhes do evento.
   * Suporte para cabeçalho de assinatura `X-MouseIA-Signature` para validação criptográfica (HMAC-SHA256).

---

## 3. Plano de Implementação

1. **Camada de Banco de Dados (Database):**
   - Definir os modelos SQLAlchemy `AuditLog` e `Webhook` em `backend/app/models/`.
   - Gerar e aplicar a migração Alembic para criar as novas tabelas.
2. **Camada de Serviços (Services):**
   - Desenvolver `backend/app/services/audit_service.py` e `backend/app/services/webhook_service.py`.
3. **Integração no Fluxo de Negócios:**
   - Registrar auditoria de login em `app/api/auth.py`.
   - Registrar auditoria de projetos/URLs e scans.
   - Disparar webhook no término do scan e na detecção de falhas críticas.
4. **Camada de API (Controllers):**
   - Expor rotas de consulta de auditoria e CRUD de webhooks.
5. **Interface Gráfica (Frontend):**
   - Adicionar uma aba de Configurações/Auditoria com a listagem dos logs de eventos.
