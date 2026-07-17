from typing import Optional
from sqlalchemy.orm import Session

from app.models.project import Project as ProjectModel
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate


class ProjectService:
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db

    def _repository(self) -> ProjectRepository:
        return ProjectRepository(self.db)

    def list_projects(self) -> list[ProjectOut]:
        projects = self._repository().list_projects()
        return [self._to_out(project) for project in projects]

    def create_project(self, payload: ProjectCreate) -> ProjectOut:
        project = self._repository().create_project(payload)
        if payload.url:
            from app.models.asset import Asset as AssetModel
            asset = AssetModel(
                name="Website Principal",
                asset_type="web_application",
                value=payload.url,
                is_active=True,
                project_id=project.id
            )
            self.db.add(asset)
            self.db.commit()
        return self._to_out(project)

    def get_project(self, project_id: int) -> Optional[ProjectOut]:
        project = self._repository().get_project(project_id)
        if project is None:
            return None
        return self._to_out(project)

    def update_project(self, project_id: int, payload: ProjectUpdate) -> Optional[ProjectOut]:
        project = self._repository().update_project(project_id, payload)
        if project is None:
            return None
        
        if payload.url is not None:
            from app.models.asset import Asset as AssetModel
            asset = self.db.query(AssetModel).filter(
                AssetModel.project_id == project_id,
                AssetModel.asset_type == "web_application"
            ).first()
            if asset:
                asset.value = payload.url
            else:
                asset = AssetModel(
                    name="Website Principal",
                    asset_type="web_application",
                    value=payload.url,
                    is_active=True,
                    project_id=project_id
                )
                self.db.add(asset)
            self.db.commit()

        return self._to_out(project)

    def delete_project(self, project_id: int) -> bool:
        return self._repository().delete_project(project_id)

    def _to_out(self, project: ProjectModel) -> ProjectOut:
        from app.models.asset import Asset as AssetModel
        assoc_asset = self.db.query(AssetModel).filter(
            AssetModel.project_id == project.id,
            AssetModel.asset_type == "web_application"
        ).first()
        url_value = assoc_asset.value if assoc_asset else None

        return ProjectOut(
            id=project.id,
            name=project.name,
            description=project.description,
            tags=list(project.tags or []),
            organization_id=project.organization_id,
            url=url_value
        )


project_service = ProjectService()
