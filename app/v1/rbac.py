#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.v1.central_db_tables import Primary_owner, Other_users
from app.v1.user_db import CreateClassTable, Database
# from os import getenv
# from app.v1 import engine, my_session

class Filter(CreateClassTable):
    def __init__(self, username, db) -> None:
        super().__init__(username, db)

    def all(self, tables=[], columns="all"):
        if not tables:
            print("Please Select at least a Table")
            return
        self.tb = tables
        self.cols = columns
        tb_cls = []
        for tb in tables:
            tb_cls.append(self.get_tbl_cls[tb])

        query = self.session.query(*tb_cls).all()  # innerjoin
         # In case you want to take care of outer or other join, you'll need this sample
        # query2 = self.session.query(*tb_cls).outerjoin(tb_cls[1], tb_cls[1].state_id == tables_clss[0].id)

        if columns == "all":
            self.__get_all_cols(query)
        else:
            self.__get_selected_cols(query)


    def __get_all_cols(self, query):
        if len(self.tb) == 1:
            tb = self.get_tbl_cls[self.tb[0]]
            # columns return value is e.g [states.id, states.name]
            columns = self.get_tb_columns(tb)
            # columns return value is now [id, name]
            columns = [col.split(".")[-1] for col in columns]
            for row in query:
                for col in columns:
                    column_data = getattr(row, col)
                    print(column_data, end="\t\t")
                print()
        else:
            for row in query:
                for each_table in row:
                    columns = self.get_tb_columns(each_table)
                    columns = [col.split(".")[-1] for col in columns]
                    for col in columns:
                        column_data = getattr(each_table, col)
                        print(column_data, end="\t\t")
                print("")
        print("")

    def __get_selected_cols(self, query):
        if len(self.tb) == 1:
            tb = self.get_tbl_cls[self.tb[0]]
            for row in query:
                for col in self.cols:
                    column_data = getattr(row, col)
                    print(column_data, end="\t\t")
                print()
        else:
            for row in query:
                for each_table in row:
                    for col in self.cols:
                        column_data = getattr(each_table, col)
                        print(column_data, end="\t\t")
                print("")
        print("")

    def col_headers(self, tables=[], columns="all") -> list:
        if not tables:
            print("Please Select at least a Table")
            return

        tb_cls = []
        for tb in tables:
            tb_cls.append(self.get_tbl_cls[tb])

        column_headers = []
        if columns == "all":
            for tb in tb_cls:
                column_headers.extend(self.get_tb_columns(tb))
        else:
            for tb in tb_cls:
                for col in self.get_tb_columns(tb):
                    if col.split(".")[-1] in columns:
                        column_headers.append(col)

        return column_headers
