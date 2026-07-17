import subprocess
import shutil
import json
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class WPScanProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "wpscan"

    def is_available(self) -> bool:
        return shutil.which("wpscan") is not None

    def scan(self, target_url: str) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        try:
            cmd = ["wpscan", "--url", target_url, "--format", "json", "--disable-tls-checks"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode not in (0, 5):  # 5 is returned by wpscan when vulns are found
                return signals

            data = json.loads(result.stdout)
            
            # WordPress Core vulnerabilities
            version_info = data.get("version", {})
            if version_info:
                signals.append({
                    "type": "wordpress_version_exposed",
                    "severity": "info",
                    "confidence": 100,
                    "desc": f"Versão exposta do WordPress: {version_info.get('number')}"
                })
                for vuln in version_info.get("vulnerabilities", []):
                    cve_list = vuln.get("references", {}).get("cve", [])
                    cve_id = cve_list[0] if cve_list else None
                    signals.append({
                        "type": "wordpress_core_vulnerability",
                        "severity": "high" if cve_id else "medium",
                        "confidence": 95,
                        "desc": f"Vulnerabilidade WordPress Core: {vuln.get('title')}",
                        "cve_id": cve_id
                    })

            # XML-RPC or admin portal exposure
            interesting = data.get("interesting_findings", [])
            for item in interesting:
                url_found = item.get("url", "")
                if "xmlrpc.php" in url_found:
                    signals.append({
                        "type": "wordpress_xmlrpc_active",
                        "severity": "medium",
                        "confidence": 100,
                        "desc": f"Protocolo XML-RPC ativado e acessível em: {url_found}"
                    })
                elif "wp-login.php" in url_found:
                    signals.append({
                        "type": "wordpress_login_exposed",
                        "severity": "low",
                        "confidence": 100,
                        "desc": f"Painel de autenticação administrativo WordPress exposto em: {url_found}"
                    })
        except Exception:
            pass
        return signals
