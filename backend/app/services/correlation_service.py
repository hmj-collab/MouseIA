from typing import Optional
from sqlalchemy.orm import Session

from app.models.finding import Finding
from app.models.vulnerability import Vulnerability
from app.models.recommendation import Recommendation


class CorrelationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def correlate_finding(self, finding: Finding, asset_id: Optional[int] = None) -> Optional[Vulnerability]:
        """
        Analyzes a new finding and correlates it with known vulnerability databases (CVE/CVSS),
        creating a Vulnerability row and its corresponding action plan (Recommendation).
        """
        # Define correlation rule map based on signal type or finding description content
        rules = {
            "wordpress_detected": {
                "title": "Exposição de Assinatura WordPress / Risco de Versão Exposta",
                "cve_id": "CVE-2023-32243",
                "cvss_score": 8.8,
                "severity": "critical",
                "description": (
                    "O WordPress expõe metatags ou pastas públicas (/wp-content) que permitem "
                    "a identificação da versão instalada, abrindo margem para enumeração e ataques "
                    "direcionados a vulnerabilidades conhecidas do core ou de plugins."
                ),
                "rec_title": "Ocultar assinatura do WordPress e restringir acesso público",
                "rec_description": (
                    "1. Remova as tags 'generator' do HTML editando o functions.php do seu tema.\n"
                    "2. Restrinja a listagem pública de pastas como /wp-content/uploads/ utilizando "
                    "regras no .htaccess ou configurações do Nginx.\n"
                    "3. Mantenha o core e todos os plugins ativamente atualizados para evitar exploits conhecidos."
                ),
                "rec_priority": "high",
            },
            "leak_server": {
                "title": "Divulgação de Informação no Cabeçalho HTTP Server",
                "cve_id": "CVE-2021-41773",
                "cvss_score": 5.3,
                "severity": "medium",
                "description": (
                    "O servidor expõe o software e a versão utilizada no cabeçalho 'Server' da resposta HTTP. "
                    "Isso permite que um atacante pesquise exploits e vulnerabilidades conhecidas para a versão exata do software."
                ),
                "rec_title": "Desativar banners de assinatura no Servidor Web",
                "rec_description": (
                    "1. No Apache, configure as diretivas: 'ServerTokens ProductOnly' e 'ServerSignature Off'.\n"
                    "2. No Nginx, configure a diretiva: 'server_tokens off' no bloco http de nginx.conf."
                ),
                "rec_priority": "medium",
            },
            "leak_x_powered_by": {
                "title": "Divulgação de Tecnologia no Cabeçalho X-Powered-By",
                "cve_id": None,
                "cvss_score": 3.7,
                "severity": "low",
                "description": (
                    "A resposta HTTP expõe o cabeçalho 'X-Powered-By' detalhando a linguagem de backend (ex: PHP, ASP.NET) "
                    "e sua versão, revelando componentes e facilitando a engenharia social ou a busca por vulnerabilidades no ecossistema."
                ),
                "rec_title": "Remover cabeçalho X-Powered-By da aplicação",
                "rec_description": (
                    "1. No PHP, edite o arquivo php.ini e defina 'expose_php = Off'.\n"
                    "2. Em aplicações Node.js/Express, desative o cabeçalho usando 'app.disable(\"x-powered-by\")' ou o middleware Helmet."
                ),
                "rec_priority": "low",
            },
            "missing_hsts": {
                "title": "Strict-Transport-Security (HSTS) não Configurado",
                "cve_id": None,
                "cvss_score": 4.3,
                "severity": "medium",
                "description": (
                    "A falta do cabeçalho Strict-Transport-Security (HSTS) deixa o canal de comunicação vulnerável a ataques "
                    "de interceptação (Man-in-the-Middle) e sequestro de sessão através de conexões HTTP comuns."
                ),
                "rec_title": "Implementar política de Strict-Transport-Security (HSTS)",
                "rec_description": (
                    "Adicione o cabeçalho 'Strict-Transport-Security: max-age=63072000; includeSubDomains; preload' "
                    "nas respostas HTTP do servidor de produção para forçar o tráfego via HTTPS."
                ),
                "rec_priority": "medium",
            },
            "missing_csp": {
                "title": "Content-Security-Policy (CSP) Ausente ou Incompleta",
                "cve_id": None,
                "cvss_score": 6.5,
                "severity": "medium",
                "description": (
                    "A ausência do cabeçalho Content-Security-Policy (CSP) permite o carregamento e execução de códigos "
                    "não autorizados no navegador do usuário, possibilitando ataques graves de injeção como Cross-Site Scripting (XSS)."
                ),
                "rec_title": "Definir e implantar cabeçalho de Content-Security-Policy",
                "rec_description": (
                    "1. Desenvolva uma política de CSP restritiva.\n"
                    "2. Comece definindo 'Content-Security-Policy: default-src 'self'' e adicione permissões apenas para fontes conhecidas de scripts, mídias e conexões."
                ),
                "rec_priority": "medium",
            },
            "missing_x_frame_options": {
                "title": "Vulnerabilidade de Clickjacking por Ausência de X-Frame-Options",
                "cve_id": None,
                "cvss_score": 4.7,
                "severity": "medium",
                "description": (
                    "A falta do cabeçalho X-Frame-Options permite que o site seja incorporado em frames de outros domínios maliciosos. "
                    "Atacantes podem usar isso para sobrepor interfaces e induzir cliques ilegítimos (Clickjacking)."
                ),
                "rec_title": "Adicionar cabeçalho de proteção de enquadramento (X-Frame-Options)",
                "rec_description": (
                    "Adicione o cabeçalho 'X-Frame-Options: SAMEORIGIN' ou a diretiva 'frame-ancestors' do CSP "
                    "nas respostas HTTP para impedir o enquadramento não autorizado."
                ),
                "rec_priority": "medium",
            }
        }

        # Try to resolve correlation rule by finding code or matching keywords in title
        matched_rule = None
        finding_title_lower = finding.title.lower()

        for key, value in rules.items():
            if key in finding_title_lower:
                matched_rule = value
                break

        # Default fallback correlation if no direct rule matches
        if not matched_rule:
            return None

        # Create Vulnerability record
        vuln = Vulnerability(
            title=matched_rule["title"],
            description=matched_rule["description"],
            severity=matched_rule["severity"],
            cvss_score=matched_rule["cvss_score"],
            cve_id=matched_rule["cve_id"],
            status="open",
            asset_id=asset_id,
            finding_id=finding.id
        )
        self.db.add(vuln)
        self.db.flush()  # populate vuln.id

        # Create corresponding action Recommendation
        rec = Recommendation(
            title=matched_rule["rec_title"],
            description=matched_rule["rec_description"],
            priority=matched_rule["rec_priority"],
            status="open",
            vulnerability_id=vuln.id
        )
        self.db.add(rec)
        self.db.commit()

        return vuln
