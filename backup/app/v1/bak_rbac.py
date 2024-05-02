#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.v1.central_db_tables import Primary_owner, Other_users
from sqlalchemy.ext.automap import automap_base
from os import getenv

class Filter:
    # The queries only central_db to find the database to be queried
    url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
        getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
    # url = "mysql+mysqldb://{}:{}@localhost:3306/{}".format(
    #     getenv("USER"), getenv("SECRET_KEY"), getenv("DATABASE"))
    __engine = create_engine(url, pool_pre_ping=True)

    def __init__(self, username: str, database: str) -> None:
        self.user = username
        self.db = database
        self.is_owner = self.get_user
        self.format = self.get_format
        session = sessionmaker(bind=Filter.__engine)()

        # Optional 1. This part checks if the database exists or not
        """
        try:
            username_data = session.query(self.user_type).filter_by(username=username).one()
            for data in username_data.db_list.values():
                if database in data:
                    print(data)
                    print("Database exist")
            # self.db = database
            # print("Database Exist")

        except Exception as e:
            print("1st Exceptipn", e)
            return
            """
        # Optional 1 Ends Here

        # This section activate the engine
        # This url queries the found database. it queries the user's database
        url = "{}://{}:{}@localhost:3306/{}".format(self.format,
            getenv("USER"), getenv("SECRET_KEY"), self.db)
        self.engine = create_engine(url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)()

    @property
    def get_user(self):
        session = sessionmaker(bind=Filter.__engine)()
        owner = session.query(Primary_owner.username).filter_by(username=self.user).one()
        if owner:
            self.user_type = Primary_owner
            session.close()
            return True
        self.user_type = Other_users
        session.close()
        return False

    @property
    def get_format(self):
        session = sessionmaker(bind=Filter.__engine)()
        db_list = session.query(self.user_type.db_list).filter_by(username=self.user).one()
        for row in db_list:
            for format, db in row.items():
                if self.db in db:
                    session.close()
                    return format
        session.close()

    def all(self, table_name, column="all"):
        classes = Create_Class(self.db, self.format, table_name).get_classes
        rows = self.session.query(classes).all()

        if column == "all":
            [print(headers, end="\t\t\t") for headers in rows[0].__dict__.keys()
            if headers != "_sa_instance_state"]
            print("")
            for row in rows:
                for column, value in row.__dict__.items():
                    if column != "_sa_instance_state":
                        print(value, end="\t\t")
                print('')
        else:
            print(column)
            for row in rows:
                column_value = getattr(row, column)
                print(column_value)


class Create_Class:
    # __engine = create_engine(url, pool_pre_ping=True)
    # db_type = {
    #     'PostgreSQL': 'postgresql',
    #     'MySQL': 'mysql+mysqldb',
    #     'Oracle': 'oracle+cx_oracle',
    #     'MicroSoftSQL': 'mysql+pyodbc',
    #     'MariaDB': None,
    #     'SQLite': None
    #     }

    def __init__(self, database: str, format, table=None) -> None:
        self.db = database
        self.format = format
        self.table_name = table
        url = "{}://{}:{}@localhost:3306/{}".format(self.format,
            getenv("USER"), getenv("SECRET_KEY"), self.db)
        self.engine = create_engine(url, pool_pre_ping=True)
        self.session = sessionmaker(bind=self.engine)()

    @property
    def get_classes(self):
        Base = automap_base()
        Base.prepare(self.engine, reflect=True)
        if not self.table_name:
            cls_table_names = Base.classes.items()
            return cls_table_names
        table_cls_name = Base.classes[self.table_name]
        self.engine.dispose()
        return table_cls_name

