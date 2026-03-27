from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
# FIXED: Pointing to the new centralized Base location
from app.models.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True) # Added to match your Schemas
    
    # Relationships
    # This links to the back_populates="project" in your Issue model
    issues = relationship("Issue", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"