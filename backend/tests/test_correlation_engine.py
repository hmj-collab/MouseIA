from sqlalchemy.orm import Session
from app.models.finding import Finding
from app.models.signal import Signal
from app.models.vulnerability import Vulnerability
from app.models.recommendation import Recommendation
from app.services.correlation_service import CorrelationService


def test_correlation_engine_grouping_and_deduplication(db_session: Session) -> None:
    # 1. Create an asset to link everything to
    from app.models.asset import Asset
    asset = Asset(
        name="Correlation Test Asset",
        asset_type="url",
        value="http://correlation-test.local",
        description="Asset used for engine grouping tests",
        is_active=True,
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)
    asset_id = asset.id

    correlation_svc = CorrelationService(db_session)

    # 2. Test Batch Grouping: Send multiple HTTP headers signals
    signals_batch_1 = [
        {"type": "missing_csp", "severity": "medium", "confidence": 95, "desc": "CSP header missing"},
        {"type": "missing_hsts", "severity": "medium", "confidence": 90, "desc": "HSTS header missing"},
        {"type": "leak_server", "severity": "low", "confidence": 85, "desc": "Server banner exposed"},
    ]

    findings_1 = correlation_svc.process_new_signals(
        signals_data=signals_batch_1,
        asset_id=asset_id,
        source="scan-headers"
    )

    # We expect EXACTLY one finding created because all these signals belong to "http_security_headers" group!
    assert len(findings_1) == 1
    finding_1 = findings_1[0]
    assert "Problemas de Configuração de Servidor Web e Cabeçalhos HTTP" in finding_1.title
    assert finding_1.severity == "medium"  # Highest severity of the signals in group
    assert finding_1.status == "open"

    # Verify that the signals in DB are correctly associated to this finding
    signals_in_db = db_session.query(Signal).filter(Signal.finding_id == finding_1.id).all()
    assert len(signals_in_db) == 3
    assert {s.signal_type for s in signals_in_db} == {"missing_csp", "missing_hsts", "leak_server"}

    # Verify that a Vulnerability was created and linked
    vuln = db_session.query(Vulnerability).filter(Vulnerability.finding_id == finding_1.id).first()
    assert vuln is not None
    assert vuln.severity == "medium"
    assert vuln.asset_id == asset_id

    # Verify Recommendation was created
    rec = db_session.query(Recommendation).filter(Recommendation.vulnerability_id == vuln.id).first()
    assert rec is not None
    assert rec.priority == "medium"

    # 3. Test Temporal Deduplication: Send a second batch with another missing header signal
    signals_batch_2 = [
        {"type": "missing_x_frame_options", "severity": "medium", "confidence": 90, "desc": "X-Frame-Options missing"},
    ]

    findings_2 = correlation_svc.process_new_signals(
        signals_data=signals_batch_2,
        asset_id=asset_id,
        source="scan-headers"
    )

    # It should reuse finding_1 instead of creating a new one!
    assert len(findings_2) == 1
    finding_2 = findings_2[0]
    assert finding_2.id == finding_1.id

    # Verify that the new signal was appended to the same finding
    signals_in_db_updated = db_session.query(Signal).filter(Signal.finding_id == finding_1.id).all()
    assert len(signals_in_db_updated) == 4
    assert any(s.signal_type == "missing_x_frame_options" for s in signals_in_db_updated)
