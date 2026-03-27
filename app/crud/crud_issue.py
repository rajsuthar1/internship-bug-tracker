from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.issue import Issue
from app.schemas.issue import IssueCreate, IssueUpdate

class CRUDIssue(CRUDBase[Issue, IssueCreate, IssueUpdate]):
    """
    CRUD object for Issue model.
    Inherits default methods (get, get_multi, create, update, remove) from CRUDBase.
    """
    
    # Custom logic to filter issues by project
    def get_by_project(self, db: Session, *, project_id: int):
        return db.query(self.model).filter(self.model.project_id == project_id).all()

# Instantiate the class so it can be imported in the routes
issue = CRUDIssue(Issue)