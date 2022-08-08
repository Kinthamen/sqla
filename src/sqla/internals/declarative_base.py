from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr

class Base:
    """Base class for DECLARATIVE_BASE"""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

DECLARATIVE_BASE = declarative_base(cls=Base)