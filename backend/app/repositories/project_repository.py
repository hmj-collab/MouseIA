from typing import Optional

from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_projects(self, organization_id: Optional[int] = None) -> list[Project]:
        q = self.db.query(Project)
        if organization_id is not None:
            q = q.filter(Project.organization_id == organization_id)
        return q.order_by(Project.id).all()

    def create_project(self, payload: ProjectCreate) -> Project:
        project = Project(
            name=payload.name,
            description=payload.description,
            tags=payload.tags or [],
            organization_id=payload.organization_id,
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_project(self, project_id: int, organization_id: Optional[int] = None) -> Optional[Project]:
        q = self.db.query(Project).filter(Project.id == project_id)
        if organization_id is not None:
            q = q.filter(Project.organization_id == organization_id)
        return q.first()

    def update_project(self, project_id: int, payload: ProjectUpdate, organization_id: Optional[int] = None) -> Optional[Project]:
        project = self.get_project(project_id, organization_id)
        if project is None:
            return None

        if payload.name is not None:
            project.name = payload.name
        if payload.description is not None:
            project.description = payload.description
        if payload.tags is not None:
            project.tags = payload.tags
        if "organization_id" in payload.model_fields_set:
            project.organization_id = payload.organization_id

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project_id: int, organization_id: Optional[int] = None) -> bool:
        project = self.get_project(project_id, organization_id)
        if project is None:
            return False

        self.db.delete(project)
        self.db.commit()
        return True
