#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from app.v1.central_db_tables import Primary_owner, Other_users
from sqlalchemy.ext.automap import automap_base
from os import getenv


class Database:
    def __init__(self, username) -> None:
        self.user = username
        url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
            getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
        engine = create_engine(url, pool_pre_ping=True)
        self.session = sessionmaker(bind=engine)()
        self.is_owner = self.get_user
        self.fmt_db_lists = self.get_fmt_db_list
        self.session.close()
        engine.dispose()

    @property
    def get_user(self):
        try:
            owner = self.session.query(Primary_owner.username).filter_by(username=self.user).one()
            return Primary_owner
        except NoResultFound as e:
            return Other_users

    @property
    def get_fmt_db_list(self): # Returns {'fmt1': [db1, db2], 'fmt2': [db3]}
        fmt_db_list = self.session.query(self.get_user.db_list).filter_by(username=self.user).one()
        fmt_db_list_dict = list(fmt_db_list)[0]
        return fmt_db_list_dict

    @property
    def get_fmt_db(self):  # returns the specific fmt_db_list {'fmt': db}
        fmt_db_lists = self.fmt_db_lists
        for fmt, db_list in fmt_db_lists.items():
            if self.db in db_list:
                self.db = self.db
                self.fmt = fmt
                return dict([(self.fmt, self.db)])

    @get_fmt_db.setter
    def get_fmt_db(self, db):
        self.db = db
        return self.db

    def get_permissions(self, db):
        if self.is_owner == Primary_owner:
            return ['ALL']
        permissions = self.session.query(Other_users.permissions).filter_by(username=self.user).one()
        # permissions[0] converts sqlalchemy instance to dict
        operations = permissions[0][db]
        return operations

    @property
    def get_db_list(self):
        db_list = self.get_fmt_db_list
        db_list = [db for db in [db_list for db_list in self.get_fmt_db_list.values()]]
        db_list = [db for dbs in self.get_fmt_db_list.values() for db in dbs]
        return db_list


class CreateClassTable(Database):
    def __init__(self, username, db) -> None:
        super().__init__(username)
        self.db = db
        self.get_fmt_db = self.db  # returns a dict of {fmt: db}
        for fmt in self.get_fmt_db.keys():
            self.fmt = fmt
        url = "{}://{}:{}@localhost:3306/{}".format(self.fmt,
            getenv("USER"), getenv("SECRET_KEY"), self.db)
        self.engine = create_engine(url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)()

    @property
    def get_tbl_cls(self) -> dict:
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        # Above provides a list of tuples [(table_name, class)]
        table_cls_names = dict(Base.classes.items()) # to give in dict fmt
        self.engine.dispose()
        return table_cls_names

    @property
    def get_tb_list(self) -> list:
        tables = list(self.get_tbl_cls.keys())
        return tables

    def get_tb_columns(self, tables=[]) -> list:
        tb_cls = self.get_tbl_cls
        tb = [tb_cls[tbs] for tbs in tb_cls.keys() if tbs in tables]
        columns = []
        for _cls in tb:
            tb_name = _cls.__table__
            tb_cols = _cls.__table__.columns.keys()
            columns.extend(f"{tb_name}.{tb_col}" for tb_col in tb_cols)
        return columns

    def close_db(self):
        self.session.close()
        self.engine.dispose()
