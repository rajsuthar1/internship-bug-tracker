from typing import Any
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    It automatically generates the table name from the class name.
    """
    id: Any
    
    # Generate __tablename__ automatically: User -> user, Issue -> issue
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()