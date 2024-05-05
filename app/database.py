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
        self.user = id
        engine = create_engine(Database.url, pool_pre_ping=True)
        self.Session = sessionmaker(bind=engine)
        self.fmt_db_list = self.get_fmt_db_list
        self.db_list = self.get_db_list

    @property
    def get_fmt_db_dt(self) -> list:
        session = self.Session()
        fmt_db_dt = session.query(UserDatabase.db_list).filter_by(id=self.user).one()
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # print(fmt_db_dt)
        # print(type(fmt_db_dt))
        if not fmt_db_dt[0]:
            session.close()
            return None
        fmt_eng_dt = []
        for key, val in fmt_db_dt.db_list.items():
            # print(key, ":", val)
            # print("--------------------------------------")
            for items in val:
                # print("===============", items)
                fmt_eng_dt.append([items[0], database[key], items[1]])
            # fmt_eng_dt.append([val[0], database[key], val[1]])
        # print(fmt_eng_dt)
        # print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        session.close()
        return fmt_eng_dt

    @property
    def get_fmt_db_list(self) -> dict: # Returns {'fmt1': [db1, db2], 'fmt2': [db3]}
        # try:
        session = self.Session()
        fmt_db_list = session.query(UserDatabase.db_list).filter_by(id=self.user).one()
        # fmt_db_list_items = json.loads(fmt_db_list.db_list)
        # fmt_db_list_items = fmt_db_list.db_list
        # print(fmt_db_list)
        # print(type(fmt_db_list))
        if not fmt_db_list[0]:
            session.close()
            return None
        fmt_db_list_dict = {}
        # print("=============&&&&&&&&&&&&&&&&&&&&&=================")
        # print(fmt_db_list)
        # print("============&&&&&&&&&&&&&&&&&&&&&&&======")
        # for row in fmt_db_list:
        for key,val in fmt_db_list[0].items():
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
        query = session.query(UserDatabase).filter_by(id=self.user)
        existing_dbs = query.one().db_list
        if not existing_dbs:
            for key, val in kwargs.items():
                kwargs[key] = list([val])
            query.update({UserDatabase.db_list: kwargs})

        else:
            if set(kwargs.keys()).issubset(existing_dbs.keys()):
                for key in kwargs.keys():
                    existing_list_of_key = existing_dbs[key]
                existing_list_of_key.append(kwargs[key])
                existing_dbs[key] = existing_list_of_key
                query.update({UserDatabase.db_list: existing_dbs})

            else:
                for key, val in kwargs.items():
                    existing_dbs[key] = [val]
                query.update({UserDatabase.db_list: existing_dbs})

        session.commit()
        session.close()



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
        self.session = sessionmaker(bind=self.engine)()
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


    def close_db(self):
        self.session.close()
        self.engine.dispose()
