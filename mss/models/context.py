# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.base import Model, Repository
from mss.models.context_type import ContextType
from mss.models.user import User
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation

class ContextRepository(Repository):
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select context_id from context')
        return [row['context_id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = Context().ids()
        applications = [Context().get(id) for id in ids]
        
        return applications

class Context(Model, ContextRepository):
    """
        Modelo da Informação de Contexto
    """
        
    __tablename__ = 'context'
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    __expires__ = {"create": ["Context.ids()"],
                   "delete": ["Context.ids()"]}
        
    id = Column('context_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("users.user_id"))
    context_type_id = Column('context_type_id', Integer, ForeignKey("context_type.context_type_id"))
    context = Column('context_txt', String)
    updated = Column('update_dt', DateTime)

    user = relation(User)
    context_type = relation(ContextType)