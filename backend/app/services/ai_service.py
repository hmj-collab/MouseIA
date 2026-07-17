import httpx
import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.vulnerability import Vulnerability

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def analyze_vulnerability(self, vulnerability_id: int) -> dict:
        """
        Analyzes a vulnerability using Google Gemini API.
        If offline, or if the API key is not configured, or if the request fails,
        it falls back to a deterministic, smart local analysis.
        """
        vuln = self.db.query(Vulnerability).filter(Vulnerability.id == vulnerability_id).first()
        if not vuln:
            return {
                "error": "Vulnerability not found"
            }

        # Check if API Key is set
        if not settings.gemini_api_key:
            logger.info("GEMINI_API_KEY is not configured. Falling back to local smart mock analysis.")
            return self._generate_mock_analysis(vuln)

        prompt = (
            f"Você é um especialista em cibersegurança do Mouse IA.\n"
            f"Analise o seguinte achado de segurança:\n"
            f"Título: {vuln.title}\n"
            f"Descrição técnica: {vuln.description}\n"
            f"Severidade: {vuln.severity}\n"
            f"CVE ID: {vuln.cve_id or 'N/A'}\n\n"
            f"Forneça as seguintes informações estruturadas em formato JSON:\n"
            f"1. Uma explicação executiva e clara da vulnerabilidade em português.\n"
            f"2. O impacto de negócio e segurança se explorada (business_impact).\n"
            f"3. Passos detalhados e práticos de remediação e hardening (remediation_steps).\n"
            f"4. Um score de confiança de detecção de 0 a 100 baseada na evidência (confidence_score).\n"
            f"5. Se este achado tem probabilidade de ser um falso positivo (is_false_positive) e a justificativa (false_positive_reason)."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.gemini_api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": {
                    "type": "OBJECT",
                    "properties": {
                        "explanation": {"type": "STRING"},
                        "business_impact": {"type": "STRING"},
                        "remediation_steps": {"type": "STRING"},
                        "confidence_score": {"type": "INTEGER"},
                        "is_false_positive": {"type": "BOOLEAN"},
                        "false_positive_reason": {"type": "STRING"}
                    },
                    "required": ["explanation", "business_impact", "remediation_steps", "confidence_score", "is_false_positive"]
                }
            }
        }

        try:
            resp = httpx.post(url, json=payload, timeout=8.0)
            if resp.status_code == 200:
                data = resp.json()
                # Parse text response from Gemini
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                import json
                return json.loads(text)
            else:
                logger.warning(f"Gemini API returned status {resp.status_code}: {resp.text}. Falling back to mock.")
        except Exception as e:
            logger.warning(f"Error calling Gemini API: {str(e)}. Falling back to mock.")

        return self._generate_mock_analysis(vuln)

    def _generate_mock_analysis(self, vuln: Vulnerability) -> dict:
        title = vuln.title.lower()
        desc = (vuln.description or "").lower()

        if "wordpress" in title or "wordpress" in desc:
            return {
                "explanation": (
                    "Instância ou componentes do WordPress expostos ou desatualizados detectados no servidor. "
                    "Atacantes usam robôs para varrer automaticamente a rede em busca destas assinaturas e "
                    "identificar vulnerabilidades conhecidas para explorar."
                ),
                "business_impact": (
                    "O comprometimento de páginas WordPress pode resultar em pichação de site (defacement), "
                    "redirecionamento de clientes para páginas maliciosas ou roubo de credenciais administrativas."
                ),
                "remediation_steps": (
                    "1. Remova tags 'generator' e assinaturas de versão no arquivo functions.php do seu tema.\n"
                    "2. Bloqueie acesso público ao diretório /wp-content/uploads/.\n"
                    "3. Restrinja o acesso a URLs sensíveis (xmlrpc.php, wp-login.php) no seu servidor Nginx/Apache."
                ),
                "confidence_score": 95,
                "is_false_positive": False,
                "false_positive_reason": ""
            }

        if "cabeçalho" in title or "header" in title or "cabeçalho" in desc:
            return {
                "explanation": (
                    "Ausência de cabeçalhos HTTP de segurança fundamentais como Content-Security-Policy (CSP) ou "
                    "Strict-Transport-Security (HSTS), ou exposição de informações de versão do software do servidor."
                ),
                "business_impact": (
                    "Facilita ataques do tipo Man-in-the-Middle (MitM) e injeções de códigos maliciosos (XSS) "
                    "no navegador do usuário, comprometendo a integridade dos dados trafegados."
                ),
                "remediation_steps": (
                    "1. Configure o servidor web para adicionar o cabeçalho 'X-Frame-Options: SAMEORIGIN'.\n"
                    "2. Ative HSTS enviando 'Strict-Transport-Security: max-age=63072000; includeSubDomains'.\n"
                    "3. Remova os cabeçalhos 'Server' e 'X-Powered-By' das respostas HTTP do servidor."
                ),
                "confidence_score": 90,
                "is_false_positive": False,
                "false_positive_reason": ""
            }

        # General Fallback
        return {
            "explanation": f"Achado técnico de vulnerabilidade do tipo {vuln.severity} detectado no ativo.",
            "business_impact": "O impacto depende do escopo de privilégios e do nível de exposição do ativo atingido.",
            "remediation_steps": "Investigue a descrição técnica do achado e aplique as melhores práticas do OWASP.",
            "confidence_score": 75,
            "is_false_positive": False,
            "false_positive_reason": ""
        }
