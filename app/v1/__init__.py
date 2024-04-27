#!/usr/bin/env python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
    getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
engine = create_engine(url, pool_pre_ping=True)
my_session = sessionmaker(bind=engine)()
