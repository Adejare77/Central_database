#!/usr/bin/python3

from sqlalchemy import String, Column, Integer, JSON, create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class UserDatabase(Base):
    __tablename__ = "user_database"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    db_list = Column(JSON, nullable=True, default=None)


if __name__ == '__main__':
    url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
        'my_user', 'my_user_passwd', 'localhost', 'central_db')
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
