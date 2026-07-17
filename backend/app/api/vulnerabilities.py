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
    user: dict[str, str] = Depends(require_role("admin", "viewer"))
) -> list[VulnerabilityOut]:
    return VulnerabilityService(db).list_vulnerabilities(asset_id=asset_id)


@router.post("", response_model=VulnerabilityOut, status_code=status.HTTP_201_CREATED)
def create_vulnerability(
    payload: VulnerabilityCreate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin"))
) -> VulnerabilityOut:
    return VulnerabilityService(db).create_vulnerability(payload)


@router.get("/{vulnerability_id}", response_model=VulnerabilityOut)
def get_vulnerability(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer"))
) -> VulnerabilityOut:
    vuln = VulnerabilityService(db).get_vulnerability(vulnerability_id)
    if vuln is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    return vuln


@router.put("/{vulnerability_id}", response_model=VulnerabilityOut)
def update_vulnerability(
    vulnerability_id: int,
    payload: VulnerabilityUpdate,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin"))
) -> VulnerabilityOut:
    vuln = VulnerabilityService(db).update_vulnerability(vulnerability_id, payload)
    if vuln is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    return vuln


@router.delete("/{vulnerability_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vulnerability(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin"))
) -> None:
    deleted = VulnerabilityService(db).delete_vulnerability(vulnerability_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")


@router.post("/{vulnerability_id}/ai-analysis")
def analyze_vulnerability_ai(
    vulnerability_id: int,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer"))
) -> dict:
    from app.services.ai_service import AIService
    vuln = VulnerabilityService(db).get_vulnerability(vulnerability_id)
    if vuln is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vulnerabilidade não encontrada")
    return AIService(db).analyze_vulnerability(vulnerability_id)


@router.get("/export/csv")
def export_vulnerabilities_csv(
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: dict[str, str] = Depends(require_role("admin", "viewer"))
):
    vulns = VulnerabilityService(db).list_vulnerabilities(asset_id=asset_id)
    
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


