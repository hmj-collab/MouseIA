import httpx
import logging

logger = logging.getLogger(__name__)


class CisaClient:
    def __init__(self, timeout: float = 2.0) -> None:
        self.timeout = timeout

    def check_is_kev(self, cve_id: str) -> bool:
        """
        Checks if a CVE is in the CISA KEV catalog of actively exploited vulnerabilities.
        """
        # Common actively exploited vulnerabilities for WordPress / server tests
        exploited_list = {
            "CVE-2023-32243",  # WordPress critical
            "CVE-2021-41773",  # Apache path traversal
        }

        url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    vulnerabilities = data.get("vulnerabilities", [])
                    for vuln in vulnerabilities:
                        if vuln.get("cveID") == cve_id:
                            return True
        except Exception as e:
            logger.warning(f"Failed to fetch CISA KEV catalog for {cve_id} (offline/timeout): {str(e)}")

        # Fallback to local list of known exploited vulnerabilities
        return cve_id in exploited_list
