from typing import Optional

from sqlalchemy.orm import Session

from app.models.site import Site as SiteModel
from app.repositories.site_repository import SiteRepository
from app.schemas.site import SiteCreate, SiteOut, SiteUpdate


class SiteService:
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def _repository(self) -> SiteRepository:
        return SiteRepository(self.db)

    def list_sites(self) -> list[SiteOut]:
        sites = self._repository().list_sites()
        return [self._to_out(site) for site in sites]

    def create_site(self, payload: SiteCreate) -> SiteOut:
        site = self._repository().create_site(payload)
        return self._to_out(site)

    def get_site(self, site_id: int) -> Optional[SiteOut]:
        site = self._repository().get_site(site_id)
        if site is None:
            return None
        return self._to_out(site)

    def update_site(self, site_id: int, payload: SiteUpdate) -> Optional[SiteOut]:
        site = self._repository().update_site(site_id, payload)
        if site is None:
            return None
        return self._to_out(site)

    def delete_site(self, site_id: int) -> bool:
        return self._repository().delete_site(site_id)

    def _to_out(self, site: SiteModel) -> SiteOut:
        return SiteOut(
            id=site.id,
            name=site.name,
            url=site.url,
            description=site.description,
            tags=list(site.tags or []),
        )


site_service = SiteService()
