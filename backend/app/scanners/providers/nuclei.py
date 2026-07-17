import subprocess
import shutil
import json
import os
import tempfile
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class NucleiProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "nuclei"

    def _local_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, "..", "modules", "nuclei", "nuclei"))

    def is_available(self) -> bool:
        if os.path.exists(self._local_path()):
            return True
        return shutil.which("nuclei") is not None

    def scan(self, target_url: str, log_callback) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            local_exe = self._local_path()
            if os.path.exists(local_exe):
                try:
                    os.chmod(local_exe, 0o755)
                except Exception:
                    pass
                cmd = [local_exe, "-target", target_url, "-json-export", temp_path, "-silent"]
            else:
                cmd = ["nuclei", "-target", target_url, "-json-export", temp_path, "-silent"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode != 0:
                log_callback("ERROR", f"Falha na execução do Nuclei (Código: {result.returncode}). Stderr: {result.stderr.strip()[:300]}")
                return signals



            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                with open(temp_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            item = json.loads(line)
                            info = item.get("info", {})
                            cve_classification = info.get("classification", {})
                            cve_id = None
                            if cve_classification:
                                cves = cve_classification.get("cve-id")
                                if isinstance(cves, list) and cves:
                                    cve_id = cves[0]
                                elif isinstance(cves, str):
                                    cve_id = cves
                            
                            severity = info.get("severity", "info").lower()
                            
                            signals.append({
                                "type": f"nuclei_{item.get('template-id', 'generic')}",
                                "severity": severity,
                                "confidence": 95,
                                "desc": f"Nuclei: {info.get('name', 'Template Match')} exposto em {item.get('matched-at')}",
                                "cve_id": cve_id
                            })
                        except Exception:
                            pass
        except Exception:
            pass
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return signals
