# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from sqlalchemy import Column, String, Integer

class ContextTypeRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass

class ContextType(Model, ContextTypeRepository):
    """
        Modelo da Informação de Contexto
    """
        
    __tablename__ = 'context_type'
        
    id = Column('context_type_id', Integer, primary_key=True)
    description = Column('description_txt', String)
    location = Column('location_txt', String)