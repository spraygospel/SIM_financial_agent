# backend/app/db_models/system_models.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'user'
    User = Column(String(16), primary_key=True)
    Name = Column(String(45), nullable=False)
    Password = Column(String(45), nullable=False)
    Role = Column(String(16), nullable=False)
    Language = Column(String(2), nullable=False)
    WhatsAppNo = Column(String(15), nullable=False)
    Email = Column(String(50), nullable=False)

class Role(Base):
    __tablename__ = 'role'
    Role = Column(String(16), primary_key=True)
    User = Column(String(16), primary_key=True)

class Menu(Base):
    __tablename__ = 'menu'
    Role = Column(String(16), primary_key=True)
    Menu = Column(String(50), primary_key=True)
    SubMenu = Column(String(50), primary_key=True)

class MenuList(Base):
    __tablename__ = 'menulist'
    Menu = Column(String(50), primary_key=True)
    SubMenu = Column(String(50), primary_key=True)
    Filename = Column(String(50), nullable=False)
    FormName = Column(String(50), nullable=False)
    Parameters = Column(String(50), nullable=True)