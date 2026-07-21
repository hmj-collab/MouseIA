import logging
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider
from app.scanners.providers.security_headers import SecurityHeadersProvider
from app.scanners.providers.wpscan import WPScanProvider
from app.scanners.providers.nuclei import NucleiProvider
from app.scanners.providers.nmap import NmapProvider
from app.scanners.providers.whatweb import WhatWebProvider
from app.scanners.providers.testssl import TestSSLProvider
from app.scanners.providers.nikto import NiktoProvider

logger = logging.getLogger(__name__)


class ScannerOrchestrator:
    def __init__(self) -> None:
        self.providers: List[BaseProvider] = [
            SecurityHeadersProvider(),
            WPScanProvider(),
            NucleiProvider(),
            NmapProvider(),
            WhatWebProvider(),
            TestSSLProvider(),
            NiktoProvider()
        ]

    def run_scan(self, target_url: str, scan_type: str, log_callback) -> List[Dict[str, Any]]:
        """
        Executes all active and available scanner providers.
        """
        scan_type = (scan_type or "todos").lower()
        signals = []
        log_callback("INFO", f"Orquestrador de Scans inicializado para {target_url}...")

        for provider in self.providers:
            # Filter based on scan type selection
            if scan_type == "wordpress":
                if provider.name not in ("wpscan", "security_headers", "whatweb"):
                    continue
            elif scan_type == "headers":
                if provider.name not in ("security_headers", "whatweb"):
                    continue
            elif scan_type in ("nmap", "port-scan"):
                if provider.name != "nmap":
                    continue
            elif scan_type in ("tls-ssl", "testssl"):
                if provider.name != "testssl":
                    continue
            elif scan_type == "nuclei":
                if provider.name != "nuclei":
                    continue
            elif scan_type == "nikto":
                if provider.name != "nikto":
                    continue
            elif scan_type in ("all", "todos"):
                # Run all providers
                pass

            log_callback("INFO", f"Verificando disponibilidade do scanner: {provider.name}...")
            if not provider.is_available():
                log_callback("WARNING", f"Scanner {provider.name} não está instalado no sistema. Ignorando.")
                continue

            log_callback("INFO", f"Executando varredura com: {provider.name}...")
            try:
                provider_signals = provider.scan(target_url, log_callback)
                signals.extend(provider_signals)
                log_callback("SUCCESS", f"Scanner {provider.name} finalizado. Encontrados {len(provider_signals)} sinais.")
                for sig in provider_signals:
                    severity_label = sig.get("severity", "info").upper()
                    log_callback("INFO", f"  -> [{severity_label}] {sig.get('desc')}")
            except Exception as e:
                log_callback("ERROR", f"Falha na varredura do provedor {provider.name}: {str(e)}")


        return signals
