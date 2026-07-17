import subprocess
import shutil
import json
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class WhatWebProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "whatweb"

    def is_available(self) -> bool:
        return shutil.which("whatweb") is not None

    def scan(self, target_url: str) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        try:
            cmd = ["whatweb", target_url, "--logging=json=-"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0 or not result.stdout:
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
