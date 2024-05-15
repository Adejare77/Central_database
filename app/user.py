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

    def check_folder(self, uploaded_files):
        home = os.path.expanduser("~/Desktop")
        central_db_dir = os.path.join(home, "central_db", self.username)
        os.makedirs(central_db_dir, exist_ok=True)

        # Extract directory name and file format
        db_name = os.path.dirname(uploaded_files[0].filename)
        file_extension = os.path.splitext(uploaded_files[0].filename)[1] # splits at "."

        formats = MyUser.acceptable_format
        for fmt in formats.keys():
            if file_extension in formats[fmt]:
                path = os.path.join(central_db_dir, db_name)
                os.makedirs(path, exist_ok=True)
                for files in uploaded_files:
                    filename = files.filename.split('/')[-1]
                    file_path = os.path.join(path, filename)
                    files.save(file_path)
                new_data = {fmt: [db_name, date.today().strftime("%Y-%m-%d")]}
                Database(self.id).upload_data(**new_data)
                return True
        return False

    def __del__(self):
        self.engine.dispose()
