#!/usr/bin/python3
'''database storage engine'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

# if getenv('HBNB_TYPE_STORAGE') == 'db':
#    from models.place import place_amenity

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    '''database storage engine for mysql storage'''
    __engine = None
    __session = None

    def __init__(self):
        '''instantiate dbstorage instance'''
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                                           getenv('HBNB_MYSQL_USER'),
                                           getenv('HBNB_MYSQL_PWD'),
                                           getenv('HBNB_MYSQL_HOST'),
                                           getenv('HBNB_MYSQL_DB')
                                       ), pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        query on the current database session
        (self.__session) all objects depending of the class
        '''
        a_dict = {}
        if cls is None:
            for i in classes.values():
                objs = self.__session.query(i).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    a_dict[key] = obj
        elif cls not in classes.values():
            return a_dict
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                a_dict[key] = obj
        return a_dict

    def new(self, obj):
        '''add the object to the current database session'''
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session obj if not None'''
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        '''reloads the database'''
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine,
                               expire_on_commit=False)
        self.__session = scoped_session(session)()

    def close(self):
        """closes session"""
        self.__session.close()
