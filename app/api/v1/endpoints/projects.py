from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import the centralized crud instance
from app import crud
# Updated: Pointing to the session file we verified earlier
from app.db.session import get_db 
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter()

@router.get("/", response_model=List[ProjectOut])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Retrieve all projects."""
    try:
        return crud.project.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate
) -> Any:
    """Create a new project."""
    try:
        return crud.project.create(db, obj_in=project_in)
    except Exception as e:
        # This will show the real error in the Swagger response body
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/{project_id}", response_model=ProjectOut)
def read_project(
    *,
    db: Session = Depends(get_db),
    project_id: int
) -> Any:
    """Get a specific project by ID."""
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project

@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate
) -> Any:
    """Update project details."""
    db_project = crud.project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return crud.project.update(db, db_obj=db_project, obj_in=project_in)

@router.delete("/{project_id}")
def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int
) -> Any:
    """Delete a project."""
    db_project = crud.project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    crud.project.remove(db, id=project_id)
    return {"status": "success", "message": "Project deleted"}