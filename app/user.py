#!/usr/bin/env python3
from app.central_db_tables import UserDatabase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class MyUser():
    def __init__(self) -> None:
        url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
            'my_user', 'my_user_passwd', 'localhost', 'central_db')
        self.engine = create_engine(url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

    def addUser(self, db=None):
        session = self.Session()
        if not db:
            new_user = UserDatabase(db_list=db)
        else:
            new_user = UserDatabase()
        session.add(new_user)
        session.commit()
        session.close()

    def delUser(self, id):
        session = self.Session()
        query = session.query(UserDatabase).filter_by(id=id).delete()
        session.commit()
        session.close()

    def __del__(self):
        self.engine.dispose()
