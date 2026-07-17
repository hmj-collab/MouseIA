import subprocess
import shutil
import json
import os
import tempfile
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class WhatWebProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "whatweb"

    def _local_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(current_dir, "..", "modules", "whatweb", "whatweb"))

    def is_available(self) -> bool:
        if os.path.exists(self._local_path()) and shutil.which("ruby") is not None:
            return True
        return shutil.which("whatweb") is not None

    def scan(self, target_url: str, log_callback) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        try:
            local_exe = self._local_path()
            if os.path.exists(local_exe) and shutil.which("ruby") is not None:
                try:
                    os.chmod(local_exe, 0o755)
                except Exception:
                    pass
                local_dir = os.path.dirname(local_exe)
                # Execute using bundle exec and run within the WhatWeb module folder
                cmd = ["bundle", "exec", "ruby", "whatweb", target_url, f"--log-json={temp_path}"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=local_dir)
            else:
                cmd = ["whatweb", target_url, f"--log-json={temp_path}"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                log_callback("ERROR", f"Falha na execução do WhatWeb (Código: {result.returncode}). Stderr: {result.stderr.strip()[:300]}")
                return signals

            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                with open(temp_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        plugins = item.get("plugins", {})
                        for plugin_name, plugin_data in plugins.items():
                            version = plugin_data.get("version")
                            # If version is list, extract first element
                            if isinstance(version, list) and version:
                                version = version[0]
                            version_info = f" (versão {version})" if version else ""
                            signals.append({
                                "type": f"whatweb_{plugin_name.lower()}",
                                "severity": "info",
                                "confidence": 100,
                                "desc": f"Identificado software/plataforma via WhatWeb: {plugin_name}{version_info}"
                            })
        except Exception as e:
            log_callback("ERROR", f"Erro no processamento do WhatWeb: {str(e)}")
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass
        return signals
