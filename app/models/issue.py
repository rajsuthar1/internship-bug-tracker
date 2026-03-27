from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# FIXED: Pointing to the new centralized Base location
from app.models.base import Base

class Issue(Base):
    # __tablename__ is handled automatically by your new Base, 
    # but we can keep it here for explicit clarity.
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    status = Column(String, default="To Do")
    
    # Relationships
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="issues")

    def __repr__(self):
        return f"<Issue(id={self.id}, title='{self.title}', status='{self.status}')>"