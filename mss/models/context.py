# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation

class ContextRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass

class Context(Model, ContextRepository):
    """
        Modelo da Informação de Contexto
    """
        
    __tablename__ = 'context'
        
    id = Column('user_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("users.user_id"))
    status = Column('status_txt', String)
    location = Column('location_txt', String)
    updated = Column('update_dt', DateTime)

    user = relation(User)