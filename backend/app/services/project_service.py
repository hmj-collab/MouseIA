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
        return self._to_out(project)

    def delete_project(self, project_id: int) -> bool:
        return self._repository().delete_project(project_id)

    def _to_out(self, project: ProjectModel) -> ProjectOut:
        return ProjectOut(
            id=project.id,
            name=project.name,
            description=project.description,
            tags=list(project.tags or []),
            organization_id=project.organization_id,
        )


project_service = ProjectService()
