# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.base import Model, Repository
from sqlalchemy import Column, String, Integer

class ApplicationRepository(Repository):
    
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select application_id from application')
        return [row['application_id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = Application().ids()
        applications = [Application().get(id) for id in ids]
        
        return applications
    
    def get_by(self,name):
        applications = Application.all()
        
        for application in applications:
            if application.name == name:
                return application
            
        return None

class Application(Model, ApplicationRepository):
    """
        Modelo de Redes Disponíveis
    """
        
    __tablename__ = 'application'
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    __expires__ = {"create": ["Application.ids()"],
                   "delete": ["Application.ids()"]}
        
    id = Column('application_id', Integer, primary_key=True)
    name = Column('name_txt', String)
    icon = Column('icon_txt', String)
    token = Column('token_txt', String)
    callback_url = Column('callback_url_txt', String)