# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.base import Model, Repository
from sqlalchemy import Column, String, Integer

class ContextTypeRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select context_type_id from context_type')
        return [row['context_type_id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = ContextType().ids()
        types = [ContextType().get(id) for id in ids]
        
        return types
    
    def get_by(self,description):
        types = ContextType().all()
        
        for context_type in types:
            if context_type.description == description:
                return context_type
            
        return None
    
class ContextType(Model, ContextTypeRepository):
    """
        Modelo da Informação de Contexto
    """
        
    __tablename__ = 'context_type'
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    __expires__ = {"create": ["ContextType.ids()"],
                   "delete": ["ContextType.ids()"]}
        
    id = Column('context_type_id', Integer, primary_key=True)
    description = Column('description_txt', String)