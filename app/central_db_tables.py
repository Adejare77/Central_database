#!/usr/bin/python3
""" Create a database table headers"""

from sqlalchemy import String, Column, Integer, JSON, create_engine
from sqlalchemy.orm import declarative_base
from os import getenv

Base = declarative_base()


class UserDatabase(Base):
    """Generate the central_db database table headers"""
    __tablename__ = "user_database"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    db_list = Column(JSON, nullable=True, default=None)


if __name__ == '__main__':
    url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
        getenv('USER'), getenv('SECRET_KEY'),
        'localhost', 'central_db')
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
