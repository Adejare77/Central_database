#!/usr/bin/python3

from sqlalchemy import String, Column, Integer, DateTime, func, JSON, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv


Base = declarative_base()

class UserDatabase(Base):
    __tablename__ = "user_database"
    id = Column(Integer, primary_key=True)
    db_list = Column(JSON, nullable=True)


if __name__ == '__main__':
    url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
        'my_user', 'my_user_passwd', 'localhost', 'central_db')
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
