from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime

from app.api.dependencies import get_db
from app.core.security import require_role
from app.models.vulnerability import Vulnerability
from app.models.project import Project
from app.models.asset import Asset
from app.models.scan import Scan

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer"))
) -> dict:
    # 1. Basic Stats Counts
    total_projects = db.query(Project).count()
    total_assets = db.query(Asset).count()
    total_scans = db.query(Scan).count()
    
    vulns = db.query(Vulnerability).all()
    total_vulns = len(vulns)
    
    # 2. Severities and status distributions
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    status_counts = {"open": 0, "mitigated": 0, "accepted": 0, "resolved": 0}
    
    resolved_vulns = []
    active_risk_scores = []
    
    for v in vulns:
        sev = (v.severity or "info").lower()
        if sev in severity_counts:
            severity_counts[sev] += 1
            
        status = (v.status or "open").lower()
        if status in status_counts:
            status_counts[status] += 1
            
        if status in ("resolved", "mitigated"):
            resolved_vulns.append(v)
            
        if status == "open" and v.risk_score is not None:
            active_risk_scores.append(v.risk_score)
            
    avg_risk_score = round(sum(active_risk_scores) / len(active_risk_scores), 2) if active_risk_scores else 0.0

    # 3. Calculate MTTR (Mean Time to Remediation) in hours
    mttr_sum = 0
    mttr_count = 0
    
    # 4. Calculate SLA Compliance
    sla_met_count = 0
    
    for v in resolved_vulns:
        if v.created_at and v.updated_at:
            delta = v.updated_at - v.created_at
            hours = delta.total_seconds() / 3600.0
            mttr_sum += hours
            mttr_count += 1
            
            # SLA Rules:
            # critical: 7 days, high: 15 days, medium: 30 days, low: 90 days
            days = delta.days
            sev = (v.severity or "info").lower()
            if sev == "critical" and days <= 7:
                sla_met_count += 1
            elif sev == "high" and days <= 15:
                sla_met_count += 1
            elif sev == "medium" and days <= 30:
                sla_met_count += 1
            elif sev in ("low", "info") and days <= 90:
                sla_met_count += 1
                
    avg_mttr_hours = round(mttr_sum / mttr_count, 1) if mttr_count > 0 else 0.0
    sla_compliance_pct = round((sla_met_count / mttr_count) * 100.0, 1) if mttr_count > 0 else 100.0

    return {
        "projects_count": total_projects,
        "assets_count": total_assets,
        "scans_count": total_scans,
        "vulnerabilities_count": total_vulns,
        "severity_counts": severity_counts,
        "status_counts": status_counts,
        "avg_risk_score": avg_risk_score,
        "avg_mttr_hours": avg_mttr_hours,
        "sla_compliance_pct": sla_compliance_pct
    }
