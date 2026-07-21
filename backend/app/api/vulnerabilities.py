from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import io
import csv
from sqlalchemy.orm import Session
from typing import Optional


from app.api.dependencies import get_db
from app.core.security import require_role
from app.schemas.vulnerability import VulnerabilityCreate, VulnerabilityOut, VulnerabilityUpdate
from app.services.vulnerability_service import VulnerabilityService

router = APIRouter(prefix="/vulnerabilities", tags=["vulnerabilities"])


@router.get("", response_model=list[VulnerabilityOut])
def list_vulnerabilities(
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
) -> list[VulnerabilityOut]:
    org_id = user.get("organization_id")
    if org_id is not None and asset_id is not None:
        from app.models.asset import Asset
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if asset and asset.organization_id != org_id:
            return []
    return VulnerabilityService(db).list_vulnerabilities(asset_id=asset_id, organization_id=org_id)


@router.post("", response_model=VulnerabilityOut, status_code=status.HTTP_201_CREATED)
def create_vulnerability(
    payload: VulnerabilityCreate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> VulnerabilityOut:
    try:
        return VulnerabilityService(db).create_vulnerability(payload, organization_id=user.get("organization_id"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{vulnerability_id}", response_model=VulnerabilityOut)
def get_vulnerability(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
) -> VulnerabilityOut:
    vuln = VulnerabilityService(db).get_vulnerability(vulnerability_id, organization_id=user.get("organization_id"))
    if vuln is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    return vuln


@router.put("/{vulnerability_id}", response_model=VulnerabilityOut)
def update_vulnerability(
    vulnerability_id: int,
    payload: VulnerabilityUpdate,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> VulnerabilityOut:
    try:
        vuln = VulnerabilityService(db).update_vulnerability(vulnerability_id, payload, organization_id=user.get("organization_id"))
        if vuln is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
        try:
            from app.models.user import User
            from app.services.audit_service import AuditService
            db_user = db.query(User).filter(User.username == user["username"]).first()
            AuditService(db).log_action(
                user_id=db_user.id if db_user else None,
                action="UPDATE_VULNERABILITY",
                target_type="vulnerability",
                target_id=vuln.id,
                details={"status": vuln.status, "severity": vuln.severity}
            )
        except Exception:
            pass
        return vuln
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{vulnerability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vulnerability(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin"))
) -> None:
    deleted = VulnerabilityService(db).delete_vulnerability(vulnerability_id, organization_id=user.get("organization_id"))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    try:
        from app.models.user import User
        from app.services.audit_service import AuditService
        db_user = db.query(User).filter(User.username == user["username"]).first()
        AuditService(db).log_action(
            user_id=db_user.id if db_user else None,
            action="DELETE_VULNERABILITY",
            target_type="vulnerability",
            target_id=vulnerability_id
        )
    except Exception:
        pass


@router.post("/{vulnerability_id}/ai-analysis")
def analyze_vulnerability_ai(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
) -> dict:
    from app.services.ai_service import AIService
    vuln = VulnerabilityService(db).get_vulnerability(vulnerability_id, organization_id=user.get("organization_id"))
    if vuln is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    return AIService(db).analyze_vulnerability(vulnerability_id)


@router.get("/export/csv")
def export_vulnerabilities_csv(
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, any] = Depends(require_role("admin", "viewer"))
):
    org_id = user.get("organization_id")
    if org_id is not None and asset_id is not None:
        from app.models.asset import Asset
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if asset and asset.organization_id != org_id:
            vulns = []
        else:
            vulns = VulnerabilityService(db).list_vulnerabilities(asset_id=asset_id, organization_id=org_id)
    else:
        vulns = VulnerabilityService(db).list_vulnerabilities(asset_id=asset_id, organization_id=org_id)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "ID", "CVE ID", "Titulo", "Descricao", "Severidade", "CVSS Score", "Risk Score", "Status", "Asset ID", "Created At"
    ])
    
    for v in vulns:
        writer.writerow([
            v.id,
            v.cve_id or "N/A",
            v.title,
            v.description or "",
            v.severity,
            v.cvss_score if v.cvss_score is not None else "",
            v.risk_score if v.risk_score is not None else "",
            v.status,
            v.asset_id or "",
            v.created_at.strftime("%Y-%m-%d %H:%M:%S") if v.created_at else ""
        ])
        
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=vulnerabilities.csv"}
    )


