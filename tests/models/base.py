from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import func
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ArrowType

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(ArrowType, default=func.now())
    updated_on = Column(ArrowType, default=func.now(), onupdate=func.now())
