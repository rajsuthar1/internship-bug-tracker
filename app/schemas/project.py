from typing import Optional
from pydantic import BaseModel, ConfigDict

# Shared properties
class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Properties to receive on Project creation
class ProjectCreate(ProjectBase):
    name: str # Name is required for creation

# Properties to receive on Project update
class ProjectUpdate(ProjectBase):
    pass

# Properties to return via API
class ProjectOut(ProjectBase):
    id: int
    # Removed owner_id because it doesn't exist in your Project model yet.
    # If you add 'owner_id' to models/project.py, you can add it back here.

    # Updated for Pydantic V2 (Industry Standard)
    model_config = ConfigDict(from_attributes=True)