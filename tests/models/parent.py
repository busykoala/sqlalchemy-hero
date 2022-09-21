from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from tests.models.base import Base


class Parent(Base):
    __tablename__ = "parent"

    name = Column(Text)
    ss_number = Column(Integer, autoincrement=True)
    children = relationship("Child")
