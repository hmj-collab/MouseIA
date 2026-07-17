import subprocess
import shutil
import json
import os
import tempfile
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class NiktoProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "nikto"

    def is_available(self) -> bool:
        return shutil.which("nikto") is not None

    def scan(self, target_url: str) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            cmd = ["nikto", "-h", target_url, "-Format", "json", "-o", temp_path]
            subprocess.run(cmd, capture_output=True, text=True, timeout=180)

            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                with open(temp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    vulns = data.get("vulnerabilities", []) or data.get("item", [])
                    if not vulns and isinstance(data, list):
                        vulns = data
                        
                    for v in vulns:
                        desc = v.get("msg", "") or v.get("description", "")
                        if not desc:
                            continue
                        
                        signals.append({
                            "type": f"nikto_{v.get('id', 'item')}",
                            "severity": "medium" if "vulnerable" in desc.lower() or "warning" in desc.lower() else "low",
                            "confidence": 90,
                            "desc": f"Nikto: {desc.strip()}"
                        })
        except Exception:
            pass
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return signals
