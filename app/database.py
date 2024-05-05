#!/usr/bin/python3
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, OperationalError
from app.central_db_tables import UserDatabase
from sqlalchemy.ext.automap import automap_base
from os import getenv
from datetime import date
import json

database = {
    "mysql+mysqldb": "MySQL",
    "postgresql": "PostgreSQL",
    "mariadb": "MariaDB",
    "sqlite": "SQLite",
    "oracle": "Oracle",
    "microsoft": "MicroSoftSQL"
}


class Database:
    url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
    def __init__(self, id) -> None:
        self.id = id
        self.engine = create_engine(Database.url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)
        self.fmt_db_list = self.get_fmt_db_list
        self.db_list = self.get_db_list

    @property
    def get_fmt_db_dt(self) -> list:
        session = self.Session()
        fmt_db_dt = session.query(UserDatabase.db_list).filter_by(id=self.id).one()
        if not fmt_db_dt[0]:
            session.close()
            return None
        fmt_eng_dt = []
        for key, val in fmt_db_dt.db_list.items():
            for items in val:
                fmt_eng_dt.append([items[0], database[key], items[1]])
        session.close()
        return fmt_eng_dt

    @property
    def get_fmt_db_list(self) -> dict: # Returns {'fmt1': [db1, db2], 'fmt2': [db3]}
        # try:
        session = self.Session()
        fmt_db_list = session.query(UserDatabase).filter_by(id=self.id).one().db_list
        if not fmt_db_list:
            session.close()
            return None
        fmt_db_list_dict = {}
        for key,val in fmt_db_list.items():
            values = []
            for element in val:
                values.append(element[0])
            fmt_db_list_dict[key] = values
        session.close()
        return fmt_db_list_dict
        # except NoResultFound:
        #     return None

    @property
    def get_fmt_db(self) -> dict:  # returns the specific fmt_db_list {'fmt': db}
        fmt_db_list = self.fmt_db_list
        for fmt, db_list in fmt_db_list.items():
            if self.db in db_list:
                self.db = self.db
                self.fmt = fmt
                return dict([(self.fmt, self.db)])
        return None

    @get_fmt_db.setter
    def get_fmt_db(self, db):
        self.db = db
        return self.db

    @property
    def get_db_list(self) -> list:
        db_list = self.fmt_db_list
        if db_list:
            db_list = [db for db in [db_list for db_list in self.fmt_db_list.values()]]
            db_list = [db for dbs in self.fmt_db_list.values() for db in dbs]
            return db_list
        return None

    def upload_data(self, **kwargs) -> list:
        session = self.Session()
        query = session.query(UserDatabase).filter_by(id=self.id).one().db_list
        for key in kwargs.keys():
            key
        if not query:
            kwargs[key] = list([kwargs[key]])
            query = kwargs

        else:
            if set(kwargs.keys()).issubset(query.keys()):
                query[key].append(kwargs[key])
                session.query(UserDatabase).filter_by(id=self.id).update({UserDatabase.db_list: query})

            else:
                kwargs[key] = list([kwargs[key]])
                query[key] = kwargs

        session.query(UserDatabase).filter_by(id=self.id).update({UserDatabase.db_list: query})
        session.commit()
        session.close()

    def del_central_database(self):
        session = self.Session()
        query = session.query(UserDatabase).filter_by(id=self.id).one().db_list
        if not query:
            session.close()
            return None
        for key in self.get_fmt_db.keys():
            key = key
        for items in query[key]:
            if self.db in items:
                query[key].remove(items)
        session.query(UserDatabase).filter_by(id=self.id).update({UserDatabase.db_list: query})
        session.commit()
        session.close()

    def __del__(self):
        self.engine.dispose()


class CreateClassTable(Database):
    def __init__(self, id, db) -> None:
        super().__init__(id)

        self.db = db
        self.get_fmt_db = self.db  # returns a dict of {fmt: db}
        if not self.get_fmt_db:
            print("Database you selected doesn't exist")
            return
        for fmt in self.get_fmt_db.keys():
            self.fmt = fmt
        url = "{}://{}:{}@localhost:3306/{}".format(self.fmt,
            getenv("USER"), getenv("SECRET_KEY"), self.db)
        self.engine = create_engine(url, pool_pre_ping=True)
        # self.Session = sessionmaker(bind=self.engine)
        self.tbl_cls = self.get_tbl_cls

    @property
    def get_tbl_cls(self) -> dict:
        try:
            Base = automap_base()
            Base.prepare(self.engine, reflect=True)
            # Above provides a list of tuples [(table_name, class)]
            table_cls_names = dict(Base.classes.items()) # to give in dict fmt
            self.engine.dispose()
        except OperationalError:
            print("Though DB is listed but not found")
            return
        return table_cls_names

    @property
    def get_tb_list(self) -> list:
        tables = list(self.tbl_cls.keys())
        return tables

    def get_tb_columns(self, tables=[]) -> list:
        tb_cls = self.tbl_cls
        tb = [tb_cls[tbs] for tbs in tb_cls.keys() if tbs in tables]
        columns = []
        for _cls in tb:
            tb_name = _cls.__table__
            tb_cols = _cls.__table__.columns.keys()
            columns.extend(f"{tb_name}.{tb_col}" for tb_col in tb_cols)
        return columns

    @property
    def del_database(self):
        query = f'DROP DATABASE IF EXISTS {self.db}'
        url = Database.url
        engine = create_engine(url, pool_pre_ping=True)
        with engine.connect() as connection:
            connection.execute(text(query))
        engine.dispose()
        self.del_central_database()

    def del_table(self, tables=[]):
        if not tables:
            return None
        if type(tables) == str:
            tables = list([tables])
        for table in tables:
            if not self.tbl_cls.get(table):
                print(f"{table} Doesn't Exist")
            else:
                tb = self.tbl_cls[table]
                tb.__table__.drop(self.engine)


    def __del__(self):
        self.engine.dispose()
