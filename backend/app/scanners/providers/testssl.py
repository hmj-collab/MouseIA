import subprocess
import shutil
import json
import os
import tempfile
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class TestSSLProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "testssl"

    def _local_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, "..", "modules", "testssl", "testssl.sh"))

    def is_available(self) -> bool:
        if os.path.exists(self._local_path()) and shutil.which("bash") is not None:
            return True
        return shutil.which("testssl.sh") is not None or shutil.which("testssl") is not None

    def scan(self, target_url: str, log_callback) -> List[Dict[str, Any]]:
        signals = []
        
        local_exe = self._local_path()
        executable = None
        if os.path.exists(local_exe) and shutil.which("bash") is not None:
            try:
                os.chmod(local_exe, 0o755)
            except Exception:
                pass
            executable = local_exe
        else:
            executable = shutil.which("testssl.sh") or shutil.which("testssl")
            
        if not executable:
            return signals

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            cmd = [executable, "--jsonfile", temp_path, target_url]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode != 0:
                log_callback("ERROR", f"Falha na execução do testssl.sh (Código: {result.returncode}). Stderr: {result.stderr.strip()[:300]}")


            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                with open(temp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        finding_id = item.get("id")
                        severity = item.get("severity", "info").lower()
                        finding_desc = item.get("finding", "")
                        
                        # Map standard severity labels
                        if severity in ("low", "medium", "high", "critical"):
                            signals.append({
                                "type": f"ssl_{finding_id.lower()}",
                                "severity": severity,
                                "confidence": 95,
                                "desc": f"testssl.sh: {finding_id} - {finding_desc}"
                            })
        except Exception:
            pass
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return signals
