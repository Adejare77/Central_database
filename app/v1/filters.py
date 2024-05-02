#!/usr/bin/python3
# from app.v1.accounts import Account
from app.v1.database import CreateClassTable
# from sqlalchemy.dialects.postgresql import JSONB


class Filter(CreateClassTable):
    def __init__(self, id, db, tables) -> None:
        super().__init__(id, db)
        self.tables = tables
        self.mapped_db = self.tbl_cls
        self.columns = None

    def table_headers(self, columns=None) -> list:
        self.columns = columns
        if type(self.tables) == str:
            self.tables = list([self.tables])
        all_tbl_headers = self.get_tb_columns(self.tables)
        if columns:
            selected_headers = [col for col in columns if col in all_tbl_headers]
            return selected_headers
        return all_tbl_headers

    def all_rows(self, columns=None):
        if not self.tables:
            print("Please Select at least a Table")
            return
        self.tb = [self.mapped_db[tbl_cls] for tbl_cls in self.mapped_db.keys() if tbl_cls in self.tables]
        query = self.session.query(*self.tb)  # innerjoin

        return self.__get_data(query, self.columns)

    def __get_data(self, query, columns):
        columns = self.table_headers(columns)
        data = []
        if len(self.tb) == 1:
            query = query.all()
            for row in query:
                _data = []
                for col in columns:
                    if row.__table__.name == col.split(".")[0]:
                        column_data = getattr(row, col.split(".")[1])
                        _data.append(column_data)
                data.append(_data)
        else:
            for i in range(1, len(self.tb)):
                query = query.join(self.tb[i])
            query = query.all()

            for row in query:
                _data = []
                for each_table in row:
                    for col in columns:
                        if col.split(".")[0] == each_table.__table__.name:
                            column_data = getattr(each_table, col.split(".")[1])
                            _data.append(column_data)
                data.append(_data)
        return data

    def del_data(self, column=None, value=None):
        if not self.tables or not column or not value:
            print("Please at least a table, a column and a value")
            return
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

    def update_data(self, table, column, value):
        tbl_cls = self.tbl_cls[table]
        query = self.session.query(table).filter_by(**{column: value})
        print("=======================")
        print(query)
        print(query.all())
        print("=======================")
        # update = query.update(tbl_cls.)
