from fastapi import APIRouter
from app.api.v1.endpoints import issues, projects

# Create the main V1 router
api_router = APIRouter()

# Include Issues endpoints
# Prefix /issues means all routes in issues.py start with /api/v1/issues
api_router.include_router(
    issues.router, 
    prefix="/issues", 
    tags=["Issues"]
)

# Include Projects endpoints
# Prefix /projects means all routes in projects.py start with /api/v1/projects
api_router.include_router(
    projects.router, 
    prefix="/projects", 
    tags=["Projects"]
)