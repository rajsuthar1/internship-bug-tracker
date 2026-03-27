from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
# FIXED: Points to the new centralized Base location
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True) # Added to match your Schemas/CRUD
    is_active = Column(Boolean, default=True)

    # Relationships
    # If you decide to link projects to owners later:
    # projects = relationship("Project", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"