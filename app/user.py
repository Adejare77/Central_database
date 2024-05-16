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
from app.sqldump import DumpCleanUp
from datetime import date


class MyUser():
    """Represents a user and provides methods for adding and
    deleting users, checking folders, and managing database connections.
    """

    def __init__(self, id, username) -> None:
        """Initializes the user's id and username

        Args:
            id (int): The unique user's id
            username (_type_): The unique user's username
        """
        url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(\
            'my_user', 'my_user_passwd', 'localhost', 'central_db')
        self.id = id
        self.username = username
        self.engine = create_engine(url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)

    def addUser(self):
        """adds a new user to central_db"""
        session = self.Session()
        new_user = UserDatabase(id=self.id, username=self.username)
        session.add(new_user)
        session.commit()
        session.close()

    def delUser(self):
        """deletes a user from the central_db"""
        session = self.Session()
        query = session.query(UserDatabase).filter_by(id=self.id).delete()
        session.commit()
        session.close()

    def check_folder(self, uploaded_files, filename, db_engine=None):
        """ checks if the sqldump file will be succesfully uploaded"""
        try:
            home = os.path.expanduser("~/Desktop")
            central_db_path = os.path.join(home, "central_db", self.username)
            os.makedirs(central_db_path, exist_ok=True)
            db_name = self.username + "_" + filename
            uploaded_files.save(os.path.join(central_db_path, filename))
            returned_fmt = DumpCleanUp(filename, db_name, central_db_path).dump_data(db_engine)
            print("===========================================")
            print("The DumpCleanUp returned: ", returned_fmt)
            print("===========================================")
            if not returned_fmt:
                return False
            new_data = {returned_fmt: [filename, date.today().strftime("%Y-%m-%d")]}
            Database(self.id).upload_data(**new_data)
            return True
        except Exception as e:
            print("=================================")
            print("** COULDN'T UPLOAD THE FILE **")
            print("=================================")
            return False

    def __del__(self):
        """Dispose the central_db engine"""
        self.engine.dispose()
