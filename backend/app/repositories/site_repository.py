from typing import Optional

from sqlalchemy.orm import Session

from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate


class SiteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_sites(self) -> list[Site]:
        return self.db.query(Site).order_by(Site.id).all()

    def create_site(self, payload: SiteCreate) -> Site:
        site = Site(
            name=payload.name,
            url=str(payload.url),
            description=payload.description,
            tags=payload.tags or [],
            company_id=payload.company_id,
        )
        self.db.add(site)
        self.db.commit()
        self.db.refresh(site)
        return site

    def get_site(self, site_id: int) -> Optional[Site]:
        return self.db.query(Site).filter(Site.id == site_id).first()

    def update_site(self, site_id: int, payload: SiteUpdate) -> Optional[Site]:
        site = self.get_site(site_id)
        if site is None:
            return None

        if payload.name is not None:
            site.name = payload.name
        if payload.url is not None:
            site.url = str(payload.url)
        if payload.description is not None:
            site.description = payload.description
        if payload.tags is not None:
            site.tags = payload.tags
        if "company_id" in payload.model_fields_set:
            site.company_id = payload.company_id

        self.db.commit()
        self.db.refresh(site)
        return site

    def delete_site(self, site_id: int) -> bool:
        site = self.get_site(site_id)
        if site is None:
            return False

        self.db.delete(site)
        self.db.commit()
        return True
