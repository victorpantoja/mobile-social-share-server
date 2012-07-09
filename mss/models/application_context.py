# coding: utf-8
#!/usr/bin/env python

from mss.models.application import Application
from mss.models.base import Model, Repository
from mss.models.context_type import ContextType

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relation


class ApplicationContextRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass


class ApplicationContext(Model, ApplicationContextRepository):
    """
        Modelo da Informação de AplicacaoContexto
    """

    __tablename__ = 'application_context'

    id = Column('id', Integer, primary_key=True)
    application_id = Column('application_id', Integer, ForeignKey("application.application_id"))
    context_type_id = Column('context_type_id', Integer, ForeignKey("context_type.context_type_id"))

    application = relation(Application)
    context_type = relation(ContextType)
