# Task: Multi-Tool Scanner Providers Engine (v0.2 - Epic 2)

## 1. Visão Geral
Esta tarefa implementa um motor modular de provedores de segurança (Scanner Providers). Em vez de rodar testes apenas via HTTPX direto, o Mouse IA atuará como um orquestrador que chama ferramentas de linha de comando (CLI) instaladas no sistema host, interpreta seus outputs estruturados (JSON/XML) e os traduz para o formato interno de **Sinais (Signals)**.

Caso uma ferramenta não esteja disponível (não instalada no PATH), o sistema fará um log de aviso e continuará a execução com os provedores ativos, garantindo resiliência.

---

## 2. Ferramentas Cadastradas e Integração

| Provedor | Função Principal | Comando Executado | Output Esperado |
| :--- | :--- | :--- | :--- |
| **SecurityHeaders** | Auditoria de cabeçalhos HTTP | Implementação nativa via HTTP client | Direct Python dict |
| **WPScan** | Scanner de WordPress | `wpscan --url <alvo> --format json` | JSON |
| **Nuclei** | Varredura de templates | `nuclei -u <alvo> -json` | JSON Lines |
| **Nikto** | Misconfigurations de servidor | `nikto -h <alvo> -Format json` | JSON |
| **Nmap + NSE** | Scanner de portas e scripts de vuln | `nmap -sV --script vuln <host> -oX -` | XML |
| **WhatWeb** | Fingerprint de tecnologias | `whatweb <alvo> --logging=json` | JSON |
| **testssl.sh** | Criptografia SSL/TLS | `testssl.sh --jsonfile <tmp> <alvo>` | JSON |

---

## 3. Arquitetura Modular

```
                  [ ScanService ]
                         │
                         ▼
             [ ScannerOrchestrator ]
             /     /     |     \     \
     [Nuclei]  [Nmap] [WPScan] [Nikto] ... (Provedores)
             \     \     |     /     /
                         ▼
               [ Sinais Consolidados ]
                         │
                         ▼
               [ Correlation Engine ]
```

### Provedor Base (`BaseProvider`):
* `name`: Propriedade identificadora do scanner.
* `is_available()`: Verifica se a ferramenta está instalada no sistema (`shutil.which`).
* `scan(target_url)`: Executa a ferramenta via subprocesso (`subprocess.Popen` com timeout) e retorna lista de dicionários contendo os Sinais.

---

## 4. Plano de Implementação

1. **Camada de Provedores (`backend/app/scanners/providers/`):**
   - Criar interface base `base.py`.
   - Desenvolver wrappers individuais (`nuclei.py`, `wpscan.py`, `nmap.py`, `whatweb.py`, `testssl.py`, `nikto.py`, `security_headers.py`).
2. **Orquestrador de Scans (`backend/app/scanners/engine/orchestrator.py`):**
   - Gerenciar o timeout global.
   - Executar apenas provedores disponíveis e coletar os sinais.
3. **Integração em `ScanService`:**
   - Modificar a execução em `backend/app/services/scan_service.py` para invocar o `ScannerOrchestrator`.
