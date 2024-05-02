#!/usr/bin/python3
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, OperationalError
from app.central_db_tables import UserDatabase
from sqlalchemy.ext.automap import automap_base
from os import getenv


class Database:
    url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
    def __init__(self, id) -> None:
        self.user = id
        engine = create_engine(Database.url, pool_pre_ping=True)
        self.session = sessionmaker(bind=engine)()
        # self.is_owner = self.get_user
        self.fmt_db_list = self.get_fmt_db_list
        self.db_list = self.get_db_list
        self.session.close()
        engine.dispose()

    @property
    def get_fmt_db_list(self) -> dict: # Returns {'fmt1': [db1, db2], 'fmt2': [db3]}
        try:
            fmt_db_list = self.session.query(UserDatabase).filter_by(id=self.user).one()
            fmt_db_list_dict = fmt_db_list.db_list
            return fmt_db_list_dict
        except NoResultFound:
            return None

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
