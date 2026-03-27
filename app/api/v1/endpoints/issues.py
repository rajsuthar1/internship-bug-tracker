from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import the centralized CRUD and dependency logic
from app import crud
from app.api.deps import get_db
from app.schemas.issue import IssueCreate, IssueOut, IssueUpdate

router = APIRouter()

@router.get("/", response_model=List[IssueOut])
def read_issues(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve all issues with pagination.
    """
    issues = crud.issue.get_multi(db, skip=skip, limit=limit)
    return issues

@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(
    *,
    db: Session = Depends(get_db),
    issue_in: IssueCreate
) -> Any:
    """
    Create a new bug/issue.
    """
    return crud.issue.create(db, obj_in=issue_in)

@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(
    *,
    db: Session = Depends(get_db),
    issue_id: int,
    issue_in: IssueUpdate
) -> Any:
    """
    Update an issue. This handles status changes and text edits.
    """
    db_issue = crud.issue.get(db, id=issue_id)
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found",
        )
    return crud.issue.update(db, db_obj=db_issue, obj_in=issue_in)

@router.get("/{issue_id}", response_model=IssueOut)
def read_issue(
    *,
    db: Session = Depends(get_db),
    issue_id: int
) -> Any:
    """
    Get a specific issue by ID.
    """
    db_issue = crud.issue.get(db, id=issue_id)
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found",
        )
    return db_issue

@router.delete("/{issue_id}", response_model=dict)
def delete_issue(
    *,
    db: Session = Depends(get_db),
    issue_id: int
) -> Any:
    """
    Delete an issue.
    """
    db_issue = crud.issue.get(db, id=issue_id)
    if not db_issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found",
        )
    crud.issue.remove(db, id=issue_id)
    return {"status": "success", "message": "Issue deleted"}