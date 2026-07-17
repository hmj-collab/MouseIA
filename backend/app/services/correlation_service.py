from typing import Optional
import datetime
from sqlalchemy.orm import Session

from app.models.finding import Finding
from app.models.vulnerability import Vulnerability
from app.models.recommendation import Recommendation
from app.models.signal import Signal as SignalModel


class CorrelationService:
    def __init__(self, db: Session) -> None:
        self.db = db

    # Grouping definitions for Correlation Engine
    GROUPS = {
        "http_security_headers": {
            "title": "Detectado: Problemas de Configuração de Servidor Web e Cabeçalhos HTTP",
            "description": "Detecção de cabeçalhos de segurança ausentes ou vazamento de informações do servidor na resposta HTTP.",
            "severity": "medium",
            "rec_title": "Implementar e corrigir cabeçalhos de segurança HTTP",
            "rec_description": (
                "Configure o servidor web para ocultar informações sensíveis e ativar cabeçalhos de segurança:\n"
                "1. Desative 'Server' e 'X-Powered-By' nas configurações do servidor (Apache/Nginx/PHP).\n"
                "2. Implemente HSTS (Strict-Transport-Security: max-age=63072000).\n"
                "3. Configure uma política CSP restritiva (Content-Security-Policy).\n"
                "4. Adicione proteção contra Clickjacking (X-Frame-Options: SAMEORIGIN)."
            ),
            "rec_priority": "medium",
            "cve_id": None,
            "cvss_score": 6.5,
        },
        "wordpress_insecure": {
            "title": "Detectado: Configuração Exposta ou Insegura do WordPress",
            "description": "Identificação de instância WordPress ativa expondo assinaturas ou páginas administrativas.",
            "severity": "critical",
            "rec_title": "Ocultar versão e restringir acesso administrativo do WordPress",
            "rec_description": (
                "1. Remova as tags 'generator' do HTML do seu tema editando o functions.php do seu tema.\n"
                "2. Restrinja o acesso público a arquivos sensíveis (xmlrpc.php, wp-login.php, .git).\n"
                "3. Desative listagem pública de diretórios em /wp-content/uploads/."
            ),
            "rec_priority": "high",
            "cve_id": "CVE-2023-32243",
            "cvss_score": 8.8,
        }
    }

    SIGNAL_TO_GROUP = {
        "missing_csp": "http_security_headers",
        "missing_hsts": "http_security_headers",
        "missing_x_frame_options": "http_security_headers",
        "leak_server": "http_security_headers",
        "leak_x_powered_by": "http_security_headers",
        
        "wordpress_detected": "wordpress_insecure",
        "wp_login_exposed": "wordpress_insecure",
        "xmlrpc_enabled": "wordpress_insecure",
        "wp_directory_listing": "wordpress_insecure",
    }

    # Individual fallback rules if not grouped
    RULES = {
        "wordpress_detected": {
            "title": "Detectado: Exposição de Assinatura WordPress / Risco de Versão Exposta",
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
                "1. Remova as tags 'generator' do HTML do seu tema editando o functions.php do seu tema.\n"
                "2. Restrinja a listagem pública de pastas como /wp-content/uploads/.\n"
                "3. Mantenha o core e todos os plugins ativamente atualizados para evitar exploits conhecidos."
            ),
            "rec_priority": "high",
        },
        "leak_server": {
            "title": "Detectado: Divulgação de Informação no Cabeçalho HTTP Server",
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
            "title": "Detectado: Divulgação de Tecnologia no Cabeçalho X-Powered-By",
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
            "title": "Detectado: Strict-Transport-Security (HSTS) não Configurado",
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
            "title": "Detectado: Content-Security-Policy (CSP) Ausente ou Incompleta",
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
            "title": "Detectado: Vulnerabilidade de Clickjacking por Ausência de X-Frame-Options",
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

    def process_new_signals(self, signals_data: list[dict], asset_id: int, source: str) -> list[Finding]:
        """
        Processes a list of raw signals, groups them into logical findings based on correlation rules,
        deduplicates against existing open findings for the asset, and triggers vulnerability enrichment.
        """
        # 1. Group signals by group key
        grouped_signals: dict[str, list[dict]] = {}
        for sig_data in signals_data:
            sig_type = sig_data["type"]
            group_key = self.SIGNAL_TO_GROUP.get(sig_type, sig_type)
            if group_key not in grouped_signals:
                grouped_signals[group_key] = []
            grouped_signals[group_key].append(sig_data)

        findings_processed = []

        # 2. Process each group
        for group_key, sigs in grouped_signals.items():
            # Get group config or individual rule as fallback
            if group_key in self.GROUPS:
                group_config = self.GROUPS[group_key]
                title = group_config["title"]
                base_description = group_config["description"]
            elif group_key in self.RULES:
                group_config = self.RULES[group_key]
                title = group_config["title"]
                base_description = group_config["description"]
            else:
                # Default fallback for untracked signals
                title = f"Detectado: Vulnerabilidade/Sinal: {group_key.replace('_', ' ').title()}"
                base_description = "Sinal de segurança bruto detectado durante a varredura automática."
                group_config = {
                    "title": title,
                    "description": base_description,
                    "severity": "info",
                    "cve_id": None,
                    "cvss_score": None,
                    "rec_title": f"Investigar sinal {group_key}",
                    "rec_description": "Revise as evidências do sinal técnico e determine a correção apropriada.",
                    "rec_priority": "low"
                }

            # Calculate severity (highest in group)
            severities = [s["severity"].lower() for s in sigs]
            severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
            max_sev = max(severities, key=lambda s: severity_order.get(s, 0))

            # Compile detailed evidence/description from all grouped signals
            desc_lines = [base_description, "\nEvidências detectadas:"]
            for sig in sigs:
                desc_lines.append(f"- [{sig['severity'].upper()}] {sig['desc']}")
            consolidated_desc = "\n".join(desc_lines)

            # 3. Check for existing open finding with same title and asset
            existing_finding = self.db.query(Finding).join(
                SignalModel, SignalModel.finding_id == Finding.id
            ).filter(
                SignalModel.asset_id == asset_id,
                Finding.status == "open",
                Finding.title == title
            ).first()

            if existing_finding:
                # Deduplication: Update existing open finding
                existing_finding.description = consolidated_desc
                existing_finding.severity = max_sev
                existing_finding.updated_at = datetime.datetime.now(datetime.timezone.utc)
                finding = existing_finding
                self.db.flush()
            else:
                # Create a new Finding
                finding = Finding(
                    title=title,
                    description=consolidated_desc,
                    severity=max_sev,
                    status="open",
                )
                self.db.add(finding)
                self.db.flush()  # populate finding.id

            # 4. Create Signal records and associate them to the Finding
            first_sig = None
            for sig_data in sigs:
                sig = SignalModel(
                    source=source,
                    signal_type=sig_data["type"],
                    severity=sig_data["severity"],
                    confidence=sig_data["confidence"],
                    description=sig_data["desc"],
                    asset_id=asset_id,
                    finding_id=finding.id
                )
                self.db.add(sig)
                if not first_sig:
                    first_sig = sig

            self.db.flush()

            # Link the legacy signal_id to the Finding (using the first signal in the group)
            # This preserves backward compatibility for the Finding schema and tests
            if not finding.signal_id and first_sig:
                finding.signal_id = first_sig.id

            self.db.flush()
            findings_processed.append(finding)

            # 5. Correlate Finding to Vulnerability and Recommendation
            self.correlate_finding(finding, asset_id=asset_id)

        self.db.commit()
        return findings_processed

    def correlate_finding(self, finding: Finding, asset_id: Optional[int] = None) -> Optional[Vulnerability]:
        """
        Analyzes a finding, checks if a vulnerability already exists,
        otherwise correlates with known CVE/CVSS mappings, and creates
        a corresponding Recommendation action plan.
        """
        # Find matching rule/group config by finding title
        matched_rule = None
        
        # Check Groups first
        for key, value in self.GROUPS.items():
            if value["title"] == finding.title:
                matched_rule = value
                break
        
        # Check individual rules next
        if not matched_rule:
            for key, value in self.RULES.items():
                if value["title"] == finding.title:
                    matched_rule = value
                    break

        if not matched_rule:
            # Fallback rule if no match found
            matched_rule = {
                "title": finding.title,
                "description": finding.description,
                "severity": finding.severity,
                "cvss_score": None,
                "cve_id": None,
                "rec_title": f"Ação Corretiva: {finding.title}",
                "rec_description": "Analisar os logs do achado e aplicar correções de segurança pertinentes.",
                "rec_priority": "medium" if finding.severity == "medium" else "low"
            }

        # Resolve CVSS, Severity and Risk Score from Threat Intelligence if cve_id is present
        cve_id = matched_rule.get("cve_id")
        cvss_score = matched_rule.get("cvss_score")
        severity = matched_rule.get("severity") or finding.severity
        risk_score = None

        if cve_id:
            try:
                from app.services.threat_intel_service import ThreatIntelService
                intel_svc = ThreatIntelService(self.db)
                cve_intel = intel_svc.get_cve_intelligence(cve_id, default_cvss=cvss_score, default_severity=severity)
                cvss_score = cve_intel.cvss_score
                severity = cve_intel.severity
                risk_score = intel_svc.calculate_risk_score(
                    cvss=cve_intel.cvss_score or 5.0,
                    epss=cve_intel.epss_score or 0.01,
                    is_kev=cve_intel.is_kev,
                    asset_id=asset_id
                )
            except Exception:
                pass

        # Calculate a basic risk score if it couldn't be resolved or if it's a general finding without CVE
        if risk_score is None:
            try:
                from app.services.threat_intel_service import ThreatIntelService
                intel_svc = ThreatIntelService(self.db)
                fallback_cvss = cvss_score or (9.0 if severity == "critical" else 7.5 if severity == "high" else 5.0 if severity == "medium" else 2.5 if severity == "low" else 1.0)
                risk_score = intel_svc.calculate_risk_score(
                    cvss=fallback_cvss,
                    epss=0.0,
                    is_kev=False,
                    asset_id=asset_id
                )
            except Exception:
                risk_score = cvss_score or 5.0

        # Check if a vulnerability already exists for this finding
        existing_vuln = self.db.query(Vulnerability).filter(Vulnerability.finding_id == finding.id).first()
        if existing_vuln:
            # Update existing vulnerability & recommendation
            existing_vuln.description = finding.description
            existing_vuln.severity = severity

            existing_vuln.cvss_score = cvss_score
            existing_vuln.risk_score = risk_score
            
            existing_rec = self.db.query(Recommendation).filter(Recommendation.vulnerability_id == existing_vuln.id).first()
            if existing_rec:
                existing_rec.title = matched_rule["rec_title"]
                existing_rec.description = matched_rule["rec_description"]
                existing_rec.priority = matched_rule["rec_priority"]
            return existing_vuln

        # Create new Vulnerability record
        vuln = Vulnerability(
            title=matched_rule["title"],
            description=finding.description,
            severity=severity,

            cvss_score=cvss_score,
            risk_score=risk_score,
            cve_id=cve_id,
            status="open",
            asset_id=asset_id,
            finding_id=finding.id
        )
        self.db.add(vuln)
        self.db.flush()  # populate vuln.id

        # Run AI False Positive Analysis automatically during ingestion
        try:
            from app.services.ai_service import AIService
            ai_svc = AIService(self.db)
            ai_res = ai_svc.analyze_vulnerability(vuln.id)
            if ai_res and not ai_res.get("error"):
                ai_details = (
                    f"\n\n--- ANÁLISE DE IA (MOUSE IA ENGINE) ---\n"
                    f"Explicação: {ai_res.get('explanation')}\n"
                    f"Impacto Comercial: {ai_res.get('business_impact')}\n"
                    f"Confiança: {ai_res.get('confidence_score')}%\n"
                )
                if ai_res.get("is_false_positive"):
                    ai_details += f"AVISO DE FALSO POSITIVO: {ai_res.get('false_positive_reason')}\n"
                    vuln.risk_score = round((vuln.risk_score or risk_score or 5.0) * 0.1, 2)
                    vuln.status = "mitigated"
                
                vuln.description = (vuln.description or "") + ai_details
        except Exception:
            pass


        # Create corresponding Recommendation action plan
        rec = Recommendation(
            title=matched_rule["rec_title"],
            description=matched_rule["rec_description"],
            priority=matched_rule["rec_priority"],
            status="open",
            vulnerability_id=vuln.id
        )
        self.db.add(rec)
        self.db.flush()

        # Trigger webhook if it is a high or critical severity vulnerability
        if vuln.severity in ("critical", "high"):
            try:
                from app.services.webhook_service import WebhookService
                WebhookService(self.db).dispatch_event("critical_vuln_found", {
                    "vulnerability_id": vuln.id,
                    "title": vuln.title,
                    "severity": vuln.severity,
                    "risk_score": vuln.risk_score,
                    "cve_id": vuln.cve_id,
                    "asset_id": vuln.asset_id
                })
            except Exception:
                pass

        return vuln

