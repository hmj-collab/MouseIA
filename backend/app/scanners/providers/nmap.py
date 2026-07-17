import subprocess
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from typing import List, Dict, Any

from app.scanners.providers.base import BaseProvider


class NmapProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "nmap"

    def is_available(self) -> bool:
        return shutil.which("nmap") is not None

    def scan(self, target_url: str) -> List[Dict[str, Any]]:
        signals = []
        if not self.is_available():
            return signals

        try:
            parsed_url = urlparse(target_url)
            host = parsed_url.hostname or parsed_url.path
            if not host:
                return signals

            # Run Nmap Service detection and vulnerability scripts returning XML output to stdout
            cmd = ["nmap", "-sV", "--script", "vuln", host, "-oX", "-"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
            
            if result.returncode != 0 or not result.stdout:
                return signals

            root = ET.fromstring(result.stdout)
            for host_el in root.findall("host"):
                for ports in host_el.findall("ports"):
                    for port in ports.findall("port"):
                        port_id = port.attrib.get("portid")
                        protocol = port.attrib.get("protocol")
                        
                        service = port.find("service")
                        service_name = service.attrib.get("name", "unknown") if service is not None else "unknown"
                        
                        for script in port.findall("script"):
                            script_id = script.attrib.get("id")
                            script_output = script.attrib.get("output", "")
                            
                            # Simple validation of script report
                            if "vulnerable" in script_output.lower() or "cve" in script_output.lower():
                                signals.append({
                                    "type": f"nmap_{script_id}",
                                    "severity": "high",
                                    "confidence": 90,
                                    "desc": f"Nmap NSE [{script_id}] detectou vulnerabilidade na porta {port_id}/{protocol} ({service_name}): {script_output.strip()}"
                                })
        except Exception:
            pass
        return signals
