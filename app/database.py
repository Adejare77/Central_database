#!/usr/bin/python3
"""Central_database Database"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, NoResultFound
from app.central_db_tables import UserDatabase
from os import getenv
import subprocess

database = {
    "mysql+mysqldb": "MySQL",
    "postgresql": "PostgreSQL",
    "mariadb": "MariaDB",
    "sqlite": "SQLite",
    "microsoft": "MicroSoftSQL"
}


class Database:
    """Establishes connection with central_db using
    """
    url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))

    def __init__(self, id) -> None:
        """ Initializes instance id

        Args:
            id (int): unique id of an instance.
        """
        self.id = id
        self.engine = create_engine(Database.url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)
        self.fmt_db_list = self.get_fmt_db_list
        self.db_list = self.get_db_list

    @property
    def get_fmt_db_dt(self) -> list:
        """Retrieves formatted database details based on user ID"""
        session = self.Session()
        fmt_db_dt = session.query(UserDatabase).filter_by(
            id=self.id).one().db_list
        if not fmt_db_dt:
            session.close()
            return None
        fmt_eng_dt = []
        for key, val in fmt_db_dt.items():
            for items in val:
                fmt_eng_dt.append([items[0], database[key], items[1]])
        session.close()
        return fmt_eng_dt


    @property
    def get_fmt_db_list(self) -> dict:
        """
        Retrieves <{formatted: [[databases]]}> dictionary based on user ID.
        """
        session = self.Session()
        try:
            fmt_db_list = session.query(UserDatabase).filter_by(
                id=self.id).one().db_list
        except NoResultFound:
            print("======================================")
            print("** USER DOES NOT EXISTS **")
            print("======================================")
            return None
    @property
    def get_fmt_db_list(self) -> dict:
        """
        Retrieves <{formatted: [[databases]]}> dictionary based on user ID.
        """
        session = self.Session()
        try:
            fmt_db_list = session.query(UserDatabase).filter_by(
                id=self.id).one().db_list
        except NoResultFound:
            print("======================================")
            print("** USER DOES NOT EXISTS **")
            print("======================================")
        if not fmt_db_list:
            session.close()
            return None
        fmt_db_list_dict = {}
        for key, val in fmt_db_list.items():
            values = []
            for element in val:
                values.append(element[0])
            fmt_db_list_dict[key] = values
        session.close()
        return fmt_db_list_dict

    @property
    def get_db_list(self) -> list:
        """Retrieves a list of databases accessible to the user."""
        db_list = self.fmt_db_list
        if db_list:
            db_list = [db for db in
                       [db_list for db_list in self.fmt_db_list.values()]]
            db_list = [db for dbs in self.fmt_db_list.values() for db in dbs]
            return db_list
        return None

    def upload_data(self, **kwargs) -> list:
        """Uploads data to the specified database"""
        session = self.Session()
        query = session.query(UserDatabase).filter_by(
            id=self.id).one().db_list
        for key in kwargs.keys():
            key
        if not query:
            kwargs[key] = list([kwargs[key]])
            query = kwargs

        else:
            if set(kwargs.keys()).issubset(query.keys()):
                query[key].append(kwargs[key])
                session.query(UserDatabase).filter_by(id=self.id).update(
                    {UserDatabase.db_list: query})

            else:
                query[key] = list([kwargs[key]])

        session.query(UserDatabase).filter_by(id=self.id).update(
            {UserDatabase.db_list: query})
        session.commit()
        session.close()

    def get_db_fmt_only(self, db) -> str:
        """Retrieves only the format of a given database"""
        fmt_db_list = self.fmt_db_list
        for fmt, db_list in fmt_db_list.items():
            if db in db_list:
                return fmt

    def del_database(self, dbs):
        """Deletes specified databases."""
        if type(dbs) == str:
            dbs = list([dbs])
        session = self.Session()
        user = session.query(UserDatabase).filter_by(
            id=self.id).one().username
        session.close()
        for db in dbs:
            dbase = user + "_" + db
            fmt = self.get_db_fmt_only(db)
            command = self.del_db_engine(fmt, dbase)
            try:
                subprocess.run(command, shell=True, check=True)
                self.__del_central_database(db)
            except subprocess.CalledProcessError:
                print("===================================")
                print("** COULD NOT DELETE DATABASE **")
                print("===================================")
                return

    def del_db_engine(self, fmt, db):
        db_engine = {
            "mysql+mysqldb": f"""
            echo 'DROP DATABASE IF EXISTS {db}' | mysql -p{getenv("SECRET_KEY")}""",
            "postgresql": f"""
            echo 'DROP DATABASE IF EXISTS {db}' | psql -U {getenv("USER")} -d central_db;"""
        }
        return db_engine[fmt]

    def __del_central_database(self, db):
        """Deletes databases associated with a user."""
        session = self.Session()
        query = session.query(UserDatabase).filter_by(
            id=self.id).one().db_list
        if not query:
            session.close()
            return None

        fmt_value = CreateClassTable(self.id, db).get_fmt_db
        for fmt in fmt_value.keys():
            key = fmt
        for items in query[key]:
            if db in items:
                query[key].remove(items)
        session.query(UserDatabase).filter_by(id=self.id).update(
            {UserDatabase.db_list: query})
        session.commit()
        session.close()

    def user(self) -> str:
        """Returns the current user username"""
        session = self.Session()
        user = session.query(UserDatabase).filter_by(
            id=self.id).one().username
        return user

    def __del__(self):
        """Cleans up resources when the object is deleted."""
        self.engine.dispose()


class CreateClassTable(Database):
    """Inherits from Database and initializes a table
    creation object based on the specified database.
    """
    def __init__(self, id, db) -> None:
        super().__init__(id)
        self.db = db
        if not self.get_fmt_db:
            print("=============================================")
            print("** COULDN'T FIND OR CONNECT TO DATABASE **")
            print("=============================================")
            return None
        for fmt in self.get_fmt_db.keys():
            self.fmt = fmt
        username = self.user()
        db = username + "_" + self.db
        url = "{}://{}:{}@localhost/{}".\
            format(self.fmt, getenv("USER"), getenv("SECRET_KEY"), db)
        try:
            self.engine = create_engine(url, pool_pre_ping=True)
            self.engine.connect()
        except OperationalError:
            print("==================================================")
            print("** COULD NOT CONNECT TO THE SELECTED DATABASE **")
            print("==================================================")
            return
        self.Session = sessionmaker(bind=self.engine)
        self.tbl_cls = self.get_tbl_cls

    @property
    def get_fmt_db(self) -> dict:
        """
        Returns the <format: db> of a specific database selected by the user
        """
        fmt_db_list = self.fmt_db_list
        for fmt, db_list in fmt_db_list.items():
            if self.db in db_list:
                self.db = self.db
                self.fmt = fmt
                return dict([(self.fmt, self.db)])
        return None

    @property
    def get_tbl_cls(self) -> dict:
        """automatically generates classes associated with to a DB using PK"""
        metadata = MetaData()
        metadata.reflect(self.engine)
        table_cls_names = dict(metadata.tables.items())
        self.engine.dispose()
        return table_cls_names

    @property
    def get_tb_list(self) -> list:
        """returns all tables of a selected DB"""
        tables = list(self.tbl_cls.keys())
        return tables

    def get_tb_columns(self, tables=[]) -> list:
        """Return the columns available for given table(s) of a DB"""
        if type(tables) != list:
            tables = list([tables])

        tb_cls = self.tbl_cls
        # tb = [tb_cls[tbs] for tbs in tb_cls.keys() if tbs in tables]
        tb = [tb_cls[tbs] for tbs in tables]
        columns = []
        for _cls in tb:
            columns.extend(_cls.c)
        columns = [f"{col}" for col in columns]
        return columns

    def del_table(self, tables=[]):
        """Delete one or more tables of a selected DB"""
        if not tables:
            return None
        if type(tables) == str:
            tables = list([tables])
        for table in tables:
            tb = self.tbl_cls[table]
            tb.drop(self.engine)

    def __del__(self):
        """Dispose Engine"""
        self.engine.dispose()
