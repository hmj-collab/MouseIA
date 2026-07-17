import subprocess
import shutil
import json
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class WhatWebProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "whatweb"

    def _local_path(self) -> str:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, "..", "modules", "whatweb", "whatweb"))

    def is_available(self) -> bool:
        import os
        if os.path.exists(self._local_path()) and shutil.which("ruby") is not None:
            return True
        return shutil.which("whatweb") is not None

    def scan(self, target_url: str, log_callback) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        try:
            import os
            local_exe = self._local_path()
            if os.path.exists(local_exe) and shutil.which("ruby") is not None:
                try:
                    os.chmod(local_exe, 0o755)
                except Exception:
                    pass
                cmd = ["ruby", local_exe, target_url, "--logging=json=-"]
            else:
                cmd = ["whatweb", target_url, "--logging=json=-"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0 or not result.stdout:
                log_callback("ERROR", f"Falha na execução do WhatWeb (Código: {result.returncode}). Stderr: {result.stderr.strip()[:300]}")
                return signals



            data = json.loads(result.stdout)
            for item in data:
                plugins = item.get("plugins", {})
                for plugin_name, plugin_data in plugins.items():
                    version = plugin_data.get("version")
                    version_info = f" (versão {version})" if version else ""
                    signals.append({
                        "type": f"whatweb_{plugin_name.lower()}",
                        "severity": "info",
                        "confidence": 100,
                        "desc": f"Identificado software/plataforma via WhatWeb: {plugin_name}{version_info}"
                    })
        except Exception:
            pass
        return signals
