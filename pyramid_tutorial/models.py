from typing import Any

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import register as register_session


db_session = scoped_session(sessionmaker())
register_session(db_session)

Base: Any = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False, default=0)
    name = Column(Text)
