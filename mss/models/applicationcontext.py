# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.application import Application
from mss.models.base import Model, Repository
from mss.models.context_type import ContextType

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relation


class ApplicationContextRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select id from application_context')
        return [row['id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = ApplicationContext().ids()
        application_context_list = [ApplicationContext().get(id) for id in ids]
        
        return application_context_list
    
    def get_by(self, application_id, context_type_id):
        application_context_list = ApplicationContext.all()
        
        for application_context in application_context_list:
            if application_context.context_type_id == context_type_id and application_context.application_id == application_id:
                return application_context
                
        return None


class ApplicationContext(Model, ApplicationContextRepository):
    """
        Modelo da Informação de AplicacaoContexto
    """

    __tablename__ = 'application_context'
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    __expires__ = {"create": ["ApplicationContext.ids()"],
                   "delete": ["ApplicationContext.ids()"]}

    id = Column('id', Integer, primary_key=True)
    application_id = Column('application_id', Integer, ForeignKey("application.application_id"))
    context_type_id = Column('context_type_id', Integer, ForeignKey("context_type.context_type_id"))

    application = relation(Application)
    context_type = relation(ContextType)
