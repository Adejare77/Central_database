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


    def header(self, table_name=[], columns="all"):
        classes = Create_Class(self.db, self.format, table_name).get_classes
        query = self.session.query(*classes)

        if len(classes) > 1:
            for i in range(1, len(table_name)):
                query = query.join(classes[i])

        rows = query.all()

        table_headers = []
        first_row_tables = rows[0]
        if len(table_name) == 1:
            table_name = rows[0].__table__
            table_columns = rows[0].__table__.columns.keys()
            table_headers.extend([f"{table_name}.{col}" for col in table_columns])

        else:
            for tables in first_row_tables:
                table_name = tables.__table__
                table_columns = tables.__table__.columns.keys()
                table_headers.extend([f"{table_name}.{col}" for col in table_columns])

        if columns == "all":
            return table_headers, table_columns  # Returns tuple of table.columns, columns

        given_table_headers = []
        for column in columns:
            val = [cols for cols in table_headers if column == cols.split(".")[1]]
            given_table_headers.extend(val)

        return given_table_headers


    def all(self, table_name=[], columns="all"):
        self.table = table_name
        self.columns = columns if columns != "all" else self.header(table_name, columns)
        classes = Create_Class(self.db, self.format, table_name).get_classes

        query = self.session.query(*classes)

        if len(classes) > 1:
            for i in range(1, len(table_name)):
                query = query.join(classes[i])

        rows = query.all()
        if columns == "all":
            for row in rows:
                if len(self.table) == 1:
                    for value in self.columns[1]:
                        column_value = getattr(row, value)
                        print(column_value, end="\t\t")
                    print()
                else:
                    for table in row:
                        for value in self.columns[1]:
                            column_value = getattr(table, value)
                            print(column_value, end="\t")
                    print("")
        else:
            for row in rows:
                if len(row) == 1:
                    row = list(row)
                for cls in row:
                    for header in self.columns:
                        column_value = getattr(cls, header)
                        print(column_value, end="\t\t")
                print()

class Create_Class:
    def __init__(self, database: str, format, tables=[]) -> None:
        self.db = database
        self.format = format
        self.table_name = tables
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

        table_cls_name = [Base.classes[table] for table in self.table_name]
        self.engine.dispose()
        return table_cls_name

