from sqlalchemy import Column, Integer, String, Boolean, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.sqltypes import Date


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


class Users(Base):
    email = Column(String, nullable=False, unique=True)
    hash_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    full_name = Column(String)
    opco_id = Column(Integer, ForeignKey('opco.id'))
    opco = relationship('Opco', back_populates='users')


class Opco(Base):
    title = Column(String, nullable=False, unique=True)
    users = relationship('Users', back_populates='opco')


class Report(Base):
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    rx = Column(Integer, nullable=False)
    tx = Column(Integer, nullable=False)
    opco = Column(String, nullable=False)
