from sqlalchemy.orm import Session
from typing import Optional, Any
import json

from app.models.audit_log import AuditLog


class AuditService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def log_action(
        self,
        user_id: Optional[int],
        action: str,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        details: Optional[Any] = None,
        ip_address: Optional[str] = None
    ) -> AuditLog:
        details_str = None
        if details is not None:
            if isinstance(details, (dict, list)):
                details_str = json.dumps(details, default=str)
            else:
                details_str = str(details)

        log_entry = AuditLog(
            user_id=user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details_str,
            ip_address=ip_address
        )
        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)
        return log_entry
