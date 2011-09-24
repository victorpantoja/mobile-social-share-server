# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from sqlalchemy import Column, String, Integer

class ApplicationRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass

class Application(Model, ApplicationRepository):
    """
        Modelo de Redes Disponíveis
    """
        
    __tablename__ = 'application'
        
    id = Column('application_id', Integer, primary_key=True)
    name = Column('name_txt', String)
    icon = Column('icon_txt', String)
    token = Column('token_txt', String)
    callback_url = Column('callback_url_txt', String)