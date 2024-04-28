#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.v1.central_db_tables import Primary_owner, Other_users
from app.v1.database import CreateClassTable, Database


class Filter(CreateClassTable):
    def __init__(self, username, db) -> None:
        super().__init__(username, db)
        self.mapped_db = self.get_tbl_cls

    def table_headers(self, tables, columns=None) -> list:
        if type(tables) == str:
            tables = list([tables])
        all_tbl_headers = self.get_tb_columns(tables)
        if columns:
            selected_headers = [col for col in columns if col in all_tbl_headers]
            return selected_headers
        return all_tbl_headers

    def all_rows(self, tables=[], columns=None):
        if not tables:
            print("Please Select at least a Table")
            return
        self.tables = tables
        self.columns = columns
        self.tb = [self.mapped_db[tbl_cls] for tbl_cls in self.mapped_db.keys() if tbl_cls in self.tables]
        query = self.session.query(*self.tb)  # innerjoin

        return self.__get_data(query, self.columns)

    def __get_data(self, query, columns):
        columns = self.table_headers(self.tables, columns)
        data = []
        if len(self.tb) == 1:
            query = query.all()
            for row in query:
                for col in columns:
                    if row.__table__.name == col.split(".")[0]:
                        column_data = getattr(row, col.split(".")[1])
                        data.append(column_data)
        else:
            for i in range(1, len(self.tb)):
                query = query.join(self.tb[i])
            query = query.all()

            for row in query:
                for each_table in row:
                    for col in columns:
                        if col.split(".")[0] == each_table.__table__.name:
                            column_data = getattr(each_table, col.split(".")[1])
                            data.append(column_data)
        return data

    def del_data(self, tables=[], column=None, value=None):
        if not tables or not column or not value:
            print("Please at least a table, a column and a value")
            return
        self.tables = tables
        self.column = column
        self.value = value
        self.tb = [self.mapped_db[tbl_cls] for tbl_cls in self.mapped_db.keys() if tbl_cls in self.tables]
        query = self.session.query(*self.tb)
        if query:
            self.__get_del(query)

    def __get_del(self, query):
        column = self.column.split(".")[1]
        if len(self.tb) == 1:
            query = query.filter_by(**{column: self.value}).all()
            if query:
                for row in query:
                    self.session.delete(row)
                    self.session.commit()
        else:
            """The purpose of "k" is very important. Since, the arrangement
            of "self.tb" is unordered, then the column to be delete might
            change. e.g if I use self.tb[0] in the getattr(), this will always refer
            to the first table column, which might be any of the table, since they don't
            follow orders. "k" tracks the using table name and then execute based
            on the giving column"""
            k = 0 # choose the first value in self.tb
            for i in range(1, len(self.tb)):
                query = query.join(self.tb[i])
                if self.tb[i].__table__.name == self.column.split(".")[0]:
                    k = i # if the table name matches the giving column name
            query = query.filter(getattr(self.tb[k], column) == self.value).all()
            if query:
                for rows in query:
                    for row in rows:
                        self.session.delete(row)
                        self.session.commit()
