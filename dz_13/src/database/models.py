from sqlalchemy import Column, Integer, String, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime, Date
from sqlalchemy.orm import declarative_base
from .db import engine

Base = declarative_base()

class Contact(Base):
    __tablename__ = "cotacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email_address = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    additional_data = Column(String(50))
    created_at = Column('created_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="cotacts")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)