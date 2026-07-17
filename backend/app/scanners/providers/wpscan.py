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
            # Execute wpscan with user (u), popular plugins (p) and popular themes (t) enumeration flags
            cmd = [
                "wpscan", 
                "--url", target_url, 
                "--format", "json", 
                "--disable-tls-checks",
                "--enumerate", "u,p,t"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode not in (0, 5):  # 5 is returned by wpscan when vulnerabilities are found
                return signals

            data = json.loads(result.stdout)
            
            # 1. WordPress Core vulnerabilities
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

            # 2. General findings (XML-RPC or login page)
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

            # 3. Enumerated Users
            users = data.get("users", {})
            if users:
                for user_key, user_val in users.items():
                    username = user_val.get("name") or user_key
                    signals.append({
                        "type": "wordpress_user_enumeration",
                        "severity": "low",
                        "confidence": 100,
                        "desc": f"Usuário WordPress enumerado via WPScan: {username}"
                    })

            # 4. Detected Plugins & Vulnerabilities
            plugins = data.get("plugins", {})
            if plugins:
                for plugin_name, plugin_val in plugins.items():
                    version = plugin_val.get("version", {}).get("number") if plugin_val.get("version") else None
                    version_info = f" (versão {version})" if version else ""
                    signals.append({
                        "type": "wordpress_plugin_detected",
                        "severity": "info",
                        "confidence": 95,
                        "desc": f"Plugin WordPress detectado: {plugin_name}{version_info}"
                    })
                    for vuln in plugin_val.get("vulnerabilities", []):
                        cves = vuln.get("references", {}).get("cve", [])
                        cve_id = cves[0] if cves else None
                        signals.append({
                            "type": "wordpress_plugin_vulnerability",
                            "severity": "high" if cve_id else "medium",
                            "confidence": 95,
                            "desc": f"Vulnerabilidade no plugin '{plugin_name}': {vuln.get('title')}",
                            "cve_id": cve_id
                        })

            # 5. Detected Themes & Vulnerabilities
            themes = data.get("themes", {})
            if themes:
                for theme_name, theme_val in themes.items():
                    version = theme_val.get("version", {}).get("number") if theme_val.get("version") else None
                    version_info = f" (versão {version})" if version else ""
                    signals.append({
                        "type": "wordpress_theme_detected",
                        "severity": "info",
                        "confidence": 95,
                        "desc": f"Tema WordPress detectado: {theme_name}{version_info}"
                    })
                    for vuln in theme_val.get("vulnerabilities", []):
                        cves = vuln.get("references", {}).get("cve", [])
                        cve_id = cves[0] if cves else None
                        signals.append({
                            "type": "wordpress_theme_vulnerability",
                            "severity": "high" if cve_id else "medium",
                            "confidence": 95,
                            "desc": f"Vulnerabilidade no tema '{theme_name}': {vuln.get('title')}",
                            "cve_id": cve_id
                        })
        except Exception:
            pass
        return signals
