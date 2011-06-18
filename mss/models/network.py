# coding: utf-8
#!/usr/bin/env python

from mss.models.base import Model, Repository
from sqlalchemy import Column, String, Integer, Boolean

class NetworkRepository(Repository):
    """
        Classe de Acesso ao Banco
    """
    pass

class Network(Model, NetworkRepository):
    """
        Modelo de Redes Disponíveis
    """
        
    __tablename__ = 'social_network'
        
    id = Column('network_id', Integer, primary_key=True)
    name = Column('name_txt', String)
    icon = Column('icon_txt', String)
    available = Column('available_bln', Boolean)