import httpx
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class SecurityHeadersProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "security_headers"

    def is_available(self) -> bool:
        return True  # Natively implemented in Python, always available!

    def scan(self, target_url: str, log_callback) -> List[Dict[str, Any]]:
        signals = []
        try:
            with httpx.Client(timeout=3.0, follow_redirects=True) as client:
                response = client.get(target_url)
                
                # Check HTTP Headers
                server = response.headers.get("Server")
                if server:
                    signals.append({
                        "type": "leak_server",
                        "severity": "medium",
                        "confidence": 90,
                        "desc": f"Header 'Server' exposto: {server}"
                    })
                
                x_powered_by = response.headers.get("X-Powered-By")
                if x_powered_by:
                    signals.append({
                        "type": "leak_x_powered_by",
                        "severity": "low",
                        "confidence": 90,
                        "desc": f"Header 'X-Powered-By' exposto: {x_powered_by}"
                    })
                
                if "Strict-Transport-Security" not in response.headers:
                    signals.append({
                        "type": "missing_hsts",
                        "severity": "low",
                        "confidence": 95,
                        "desc": "Header de segurança 'Strict-Transport-Security' (HSTS) ausente."
                    })
                
                if "X-Frame-Options" not in response.headers:
                    signals.append({
                        "type": "missing_x_frame_options",
                        "severity": "low",
                        "confidence": 95,
                        "desc": "Header de segurança 'X-Frame-Options' ausente (risco de Clickjacking)."
                    })
                
                if "Content-Security-Policy" not in response.headers:
                    signals.append({
                        "type": "missing_csp",
                        "severity": "medium",
                        "confidence": 95,
                        "desc": "Header de segurança 'Content-Security-Policy' (CSP) ausente."
                    })

                # Check WordPress signature (as a basic check)
                body = response.text.lower()
                if "wp-content" in body or "wp-includes" in body or "generator\" content=\"wordpress" in body:
                    signals.append({
                        "type": "wordpress_detected",
                        "severity": "info",
                        "confidence": 100,
                        "desc": "Assinatura do WordPress detectada no código HTML do site."
                    })
        except Exception:
            pass
        return signals
