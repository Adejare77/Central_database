#!/usr/bin/env python3
"""This module provides a class MyUser for managing users and
their associated data in the central_db database. It also includes
utility functions for interacting with the database and file system.
"""
from central_db_tables import UserDatabase
from app.database import Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import subprocess
from app.sqldump import DumpCleanUp
from os import getenv
from datetime import date

class MyUser():
    """Represents a user and provides methods for adding and
    deleting users, checking folders, and managing database connections.
    """
    acceptable_format = {
        "mysql+mysqldb": ['.frm', '.ibd', '.myd', '.myi', '.ibdata'],
        "postgresql": ['.pgsql', '.pgdata', '.sql', '.dump'],
        "sqlite": ['.sqlite', '.db', '.sqlite3'],
        "microsoft": ['.mdf', '.ldf', '.bak', '.ndf'],
        "oracle": ['.log', '.dbf', '.ctl'],
        "mariadb": ['.ibd', '.frm']
        }
    server_path = {
        "mysql+mysqldb": "/var/lib/mysql/",
    }
    def __init__(self, id, username) -> None:
        url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
            'my_user', 'my_user_passwd', 'localhost', 'central_db')
        self.id = id
        self.username = username
        self.engine = create_engine(url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

    def addUser(self):
        session = self.Session()
        new_user = UserDatabase(id=self.id, username=self.username)
        session.add(new_user)
        session.commit()
        session.close()

    def delUser(self):
        session = self.Session()
        query = session.query(UserDatabase).filter_by(id=self.id).delete()
        session.commit()
        session.close()

    def check_folder(self, uploaded_files, filename, db_engine=None):
        try:
            # filename = uploaded_files.filename
            home = os.path.expanduser("~/Desktop")
            central_db_path = os.path.join(home, "central_db", self.username)
            os.makedirs(central_db_path, exist_ok=True)
            # path = os.path.join(central_db_dir, filename)
            db_name = self.username + "_" + filename
            # uploaded_files.save(path)
            uploaded_files.save(os.path.join(central_db_path, filename))
            returned_fmt = DumpCleanUp(filename, db_name, central_db_path).dump_data(db_engine)
            if not returned_fmt:
                return False
            new_data = {returned_fmt: [filename, date.today().strftime("%Y-%m-%d")]}
            Database(self.id).upload_data(**new_data)
            return True
        except Exception as e:
            return False

    def __del__(self):
        self.engine.dispose()
