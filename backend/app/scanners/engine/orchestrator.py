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
        signals = []
        log_callback("INFO", f"Orquestrador de Scans inicializado para {target_url}...")

        for provider in self.providers:
            # Filter based on scan type selection
            if scan_type == "wordpress" and provider.name not in ("wpscan", "security_headers", "whatweb"):
                continue

            log_callback("INFO", f"Verificando disponibilidade do scanner: {provider.name}...")
            if not provider.is_available():
                log_callback("WARNING", f"Scanner {provider.name} não está instalado no sistema. Ignorando.")
                continue

            log_callback("INFO", f"Executando varredura com: {provider.name}...")
            try:
                provider_signals = provider.scan(target_url, log_callback)
                signals.extend(provider_signals)
                log_callback("SUCCESS", f"Scanner {provider.name} finalizado. Encontrados {len(provider_signals)} sinais.")
            except Exception as e:
                log_callback("ERROR", f"Falha na varredura do provedor {provider.name}: {str(e)}")

        return signals
