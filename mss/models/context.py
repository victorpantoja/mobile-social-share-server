# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from mss.models.user import User
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation
from mss.models.context_type import ContextType

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
    context_type_id = Column('context_type_id', Integer, ForeignKey("context_type.context_type_id"))
    updated = Column('update_dt', DateTime)

    user = relation(User)
    context_type = relation(ContextType)