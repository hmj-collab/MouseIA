# Capítulo 3: Guia de Funcionalidades e Operação

Este capítulo explica o funcionamento operacional das principais áreas do sistema Mouse IA, cobrindo o gerenciamento de acesso, a definição de escopo e o pipeline de varreduras técnicas.

---

## 1. Controle de Acesso (RBAC) e Autenticação
O Mouse IA implementa controle de acesso baseado em cargos (RBAC) para garantir a segurança dos dados. O acesso é autenticado via tokens JWT (JSON Web Tokens).

### Cargos e Níveis de Permissão
* **Administrador (`admin`):**
  * Acesso irrestrito a todos os recursos.
  * Adicionar/Editar/Deletar Organizações, Projetos e Usuários.
  * Iniciar varreduras e alterar o status de mitigação de vulnerabilidades.
* **Visualizador (`viewer`):**
  * Acesso de leitura.
  * Consultar Dashboards, visualizar a lista de projetos, checar vulnerabilidades e ler relatórios gerados por IA.
  * Não pode deletar registros ou iniciar novas varreduras.

---

## 2. Gestão de Escopo: Organizações e Projetos
O escopo define a superfície de ataque que a plataforma está autorizada a monitorar.

```
Organização (Empresa Cliente)
      │
      ▼
Projeto (Escopo Lógico / Unidade de Negócio)
      │
      ▼
Endereço de Destino (URL do Alvo)
```

### Fluxo Operacional:
1. **Organização (Ex: Grupo Alpha SA):** Representa o cliente final ou empresa controladora.
2. **Projeto (Ex: E-commerce Principal):** Um agrupador lógico contendo o escopo técnico.
3. **Endereço de Destino (URL) obrigatório:** Ao cadastrar um Projeto, o usuário deve preencher obrigatoriamente a URL alvo (ex: `https://meusite.com`). 
   * *O backend intercepta este campo e cria automaticamente um Ativo Técnico (Asset) do tipo `web_application` vinculado a esse projeto.*

---

## 3. Execução de Varreduras (Scan Pipeline)
O pipeline de varreduras do Mouse IA realiza testes de segurança ativos contra as URLs de destino cadastradas nos Projetos.

### Como Iniciar um Scan:
1. Acesse o menu **Varreduras (Scans)**.
2. Clique em **Executar Novo Scan**.
3. Selecione o **Projeto** desejado (o qual já contém o endereço de destino).
4. Selecione o **Tipo de Análise** (`web_headers` ou `wordpress`).
5. Clique em **Iniciar Varredura**.

### Varreduras Ativas Efetuadas:
* **web_headers (Auditoria de Cabeçalhos HTTP):**
  * Verifica vazamentos de informação (headers `Server` ou `X-Powered-By`).
  * Valida a ausência de cabeçalhos fundamentais de segurança (`Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`).
  * Testa proteção contra Directory Listing em rotas conhecidas.
  * Verifica vazamentos de repositórios confidenciais (ex: `.git/config`).
* **wordpress (Auditoria WordPress):**
  * Varre o HTML buscando meta-tags e diretórios `/wp-content` ou `/wp-includes`.
  * Testa a exposição de painéis administrativos (`/wp-login.php`).
  * Testa se o protocolo `xmlrpc.php` está ativo (risco de força bruta e amplificação DDoS).

---

## 4. Correlation Engine (Sinais vs Vulnerabilidades)
Quando o Scanner conclui a varredura, ele gera **Sinais (Signals)** técnicos brutos. O **Correlation Engine** processa esses sinais e realiza:

* **Agrupamento por Regra:** Agrupa sinais relacionados temporariamente sob a mesma causa raiz (ex: sinais de headers CSP e HSTS ausentes são agrupados em uma única vulnerabilidade de *"Problemas de Configuração de Cabeçalhos HTTP"*).
* **Deduplicação Temporal:** Se um sinal repetido é ingerido no mesmo ativo e já existe uma vulnerabilidade aberta correspondente, a vulnerabilidade existente é atualizada em vez de criar uma duplicada, mantendo o histórico conciso.
