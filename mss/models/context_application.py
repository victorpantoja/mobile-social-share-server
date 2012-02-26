# coding: utf-8
#!/usr/bin/env python

from mss.models.application import Application
from mss.models.base import Model, Repository
from mss.models.context import Context

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relation


class ContextApplicationRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass


class ContextApplication(Model, ContextApplicationRepository):
    """
        Modelo da Informação de Contexto
    """

    __tablename__ = 'context_application'

    id = Column('id', Integer, primary_key=True)
    context_id = Column('context_id', Integer, ForeignKey("context.context_id"))
    application_id = Column('application_id', Integer, ForeignKey("application.application_id"))

    context = relation(Context)
    application = relation(Application)
