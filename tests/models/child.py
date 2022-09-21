from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from tests.models.base import Base


class Child(Base):
    __tablename__ = "child"

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))
