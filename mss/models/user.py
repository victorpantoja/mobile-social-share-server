# coding: utf-8
#!/usr/bin/env python

from mss.core import meta
from mss.core.cache import cached, CachedExtension
from mss.models.base import Model, Repository
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relation


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

    def get_by(self, username):
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

    __tablename__ = 'auth_user'

    __mapper_args__ = {'extension': CachedExtension()}

    __expires__ = {"create": ["User.ids()"],
                   "delete": ["User.ids()"]}

    id = Column('id', Integer, primary_key=True)
    last_name = Column('last_name', String)
    first_name = Column('first_name', String)
    username = Column('username', String)
    email = Column('email', String)
    is_staff = Column('is_staff', Integer)
    is_superuser = Column('is_superuser', Integer)
    is_active = Column('is_active', Integer)
    created = Column('date_joined', DateTime)
    last_login = Column('last_login', DateTime)
    password = Column('password', String)


class UserProfile(Model, UserRepository):
    """
        Modelo de Usuário
    """

    _FEMALE = 'F'
    _MALE = 'M'
    _OTHER = 'O'

    __tablename__ = 'user_profile'

    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("auth_user.id"))
    gender = Column('gender_flg', String)
    token = Column('token_txt', String)
    user = relation(User, primaryjoin=user_id == User.id)
