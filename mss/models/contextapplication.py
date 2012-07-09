# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.application import Application
from mss.models.base import Model, Repository
from mss.models.context import Context

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relation


class ContextApplicationRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select id from context_application')
        return [row['id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = ContextApplication().ids()
        contexts = [ContextApplication().get(id) for id in ids]

        return contexts
        
    def get_by(self, application_id):
        context_application_list = []
        
        contexts = ContextApplication.all()

        for context_application in contexts:
            if context_application.application_id == application_id:
                context_application_list.append(context_application)

        return context_application_list

class ContextApplication(Model, ContextApplicationRepository):
    """
        Modelo da Informação de Contexto
    """

    __tablename__ = 'context_application'

    __mapper_args__ = {'extension': CachedExtension()}

    __expires__ = {"create": ["ContextApplication.ids()"],
                   "delete": ["ContextApplication.ids()"]}

    id = Column('id', Integer, primary_key=True)
    context_id = Column('context_id', Integer, ForeignKey("context.context_id"))
    application_id = Column('application_id', Integer, ForeignKey("application.application_id"))

    context = relation(Context)
    application = relation(Application)
