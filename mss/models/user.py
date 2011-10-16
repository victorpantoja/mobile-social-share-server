# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.base import Model, Repository
from sqlalchemy import Column, String, DateTime, Integer


class UserRepository(Repository):
    
    @cached
    def ids(self):
        session = meta.get_session()
        result = session.execute('select user_id from users')
        return [row['user_id'] for row in result.fetchall()]

    @staticmethod
    def all():
        ids = User().ids()
        applications = [User().get(id) for id in ids]
        
        return applications
    
    def get_by(self,username):
        users = User.all()
        
        for user in users:
            if user.username == username:
                return user
            
        return None

class User(Model, UserRepository):
    """
        Modelo de Usuário
    """
        
    _FEMALE = 'F'
    _MALE = 'M'
    _OTHER = 'O'
    
    __tablename__ = 'users'
    
    __mapper_args__ = {'extension': CachedExtension()}
    
    __expires__ = {"create": ["User.ids()"],
                   "delete": ["User.ids()"]}
        
    id = Column('user_id', Integer, primary_key=True)
    last_name = Column('lastname_txt', String)
    first_name = Column('firstname_txt', String)
    username = Column('username_txt', String)
    gender = Column('gender_flg', String)
    created = Column('criate_dt', DateTime)
    last_login = Column('lastlogin_dt', DateTime)
    password = Column('password_txt', String)