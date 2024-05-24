#!/usr/bin/python3
""" Create a database table headers"""

from sqlalchemy import String, Column, Integer, JSON, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import subprocess
from app import users_path
from app.sqldump import DumpCleanUp
from datetime import date


Base = declarative_base()


class UserDatabase(Base):
    """Generate the central_db database table headers"""
    __tablename__ = "user_database"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    db_list = Column(JSON, nullable=True, default=None)

    def __init__(self, id, username):
        self.id = id
        self.username = username

        url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
            os.getenv('USER'), os.getenv('SECRET_KEY'),
            'localhost', 'central_db')
        self.engine = create_engine(url, pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = Session()

    def addUser(self):
        """adds a new user to central_db"""
        self.session.add(self)
        self.session.commit()
        self.session.close()

    def delUser(self):
        """deletes a user from the central_db"""
        try:
            self.session.query.filter_by(id=self.id).delete()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
        finally:
            self.session.close()

    def check_folder(self, uploaded_files, filename, db_engine=None):
        """ checks if the sqldump file will be succesfully uploaded"""
        from app.database import Database

        try:
            central_db_path = os.path.join(users_path, self.username)
            os.makedirs(central_db_path, exist_ok=True)
            db_name = self.username + "_" + filename
            uploaded_files.save(os.path.join(central_db_path,
                                             filename + ".sql"))
            temp_folder = os.path.join(central_db_path, "temp")
            returned_fmt = DumpCleanUp(filename, db_name,
                                       central_db_path).dump_data(db_engine)
            if os.path.exists(temp_folder):
                subprocess.run(f'rm -r {temp_folder}', check=True, shell=True)
            if not returned_fmt:
                return False
            new_data = {returned_fmt:
                        [filename, date.today().strftime("%Y-%m-%d")]}
            Database(self.id).upload_data(**new_data)
            return True
        except Exception as e:
            error = "** COULDN'T UPLOAD THE FILE **"
            print("============", error, "===========", sep="\n")
            if os.path.exists(temp_folder):
                subprocess.run(f'rm -r {temp_folder}', check=True, shell=True)
            return False




if __name__ == '__main__':
    url = 'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
        os.getenv('USER'), os.getenv('SECRET_KEY'),
        'localhost', 'central_db')
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
