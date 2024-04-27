#!/usr/bin/python3

from sqlalchemy import String, Column, Integer, DateTime, func, JSON, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class User_info(Base):
    __tablename__ = "client_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)
    full_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    registered_date = Column(DateTime, default=func.now())
    Organization_name = Column(String(128), nullable=True)
    database = Column(JSON, nullable=True)

class Primary_owner(Base):
    __tablename__ = "authoritative_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    db_list = Column(JSON, nullable=False)

class Other_users(Base):
    __tablename__ = "other_users"
    owner_id = Column(Integer, ForeignKey("authoritative_user.id"), nullable=False)
    owner = Column(String(128), primary_key=True, nullable=False, unique=True)
    username = Column(String(128), nullable=False)
    permissions = Column(JSON, nullable=True)
    db_list = Column(JSON, nullable=False)

# class Data(Base):
#     __tablename__ = "databases"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(128), ForeignKey("authoritative_user.username"), nullable=False)
#     db_type = Column(String(60), nullable=False)
#     db_list = Column(JSON, nullable=False)


if __name__ == '__main__':
    url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
        'my_user', 'my_user_passwd', 'localhost', 'central_db')
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
