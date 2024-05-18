#!/usr/bin/python3
"""The Filter Module"""
from app.database import CreateClassTable
from sqlalchemy import text


class Filter(CreateClassTable):
    """Processes Queries issued"""
    def __init__(self, id, db, tables, columns=None) -> None:
        """Instantiate id, database, tables and columns

        Args:
            id (int): unique id of a user
            db (str): database selected
            tables (list): tables to be queried in the DB selected
            columns (str, optional): Tables column to display.
            Defaults to None.
        """
        super().__init__(id, db)
        if type(tables) == str:
            tables = list([tables])
        self.tables = tables
        try:
            self.mapped_db = self.tbl_cls
        except AttributeError:
            print("** DATABASE DOES NOT EITHER EXISTS OR COULDN'T CONNECT **")
            return
        if columns and type(columns) == str:
            columns = list([columns])
        self.columns = columns
        self.tbl_headers = self.table_headers(self.tables, self.columns)

    def table_headers(self, tables, columns) -> list:
        """table headers to be displayed"""
        if type(tables) == str:
            tables = list([tables])
        if type(columns) == str:
            columns = list([columns])
        all_tbl_headers = self.get_tb_columns(tables)
        if columns:
            # selected_headers = [col for col in columns
            #                     if col in all_tbl_headers]
            selected_headers = [col for col in all_tbl_headers
                                if col in columns]
            return selected_headers
        self.columns = all_tbl_headers
        return all_tbl_headers

    def all_rows(self, join_type=None, conditions=[[]]):
        """queries all rows"""
        self.tb = [self.mapped_db[tbl_cls] for tbl_cls in self.tables]
        if len(self.tb) == 1:
            return self.__one_table(self.tb)
        return self.__multiple_tables(self.tb, join_type, conditions)

    def __one_table(self, tbl_cls):
        """Returns from single selected table"""
        session = self.Session()
        query = session.query(*tbl_cls).all()
        data = []
        for row in query:
            row_data = []
            for col in self.columns:
                column_data = getattr(row, col.split(".")[1])
                row_data.append(column_data)
            data.append(row_data)
        session.close()
        return data

    def __multiple_tables(self, tbl_clss, join_type, conditions):
        """Returns from multiple selected tables """
        session = self.Session()
        data = []
        query = session.query(*tbl_clss)
        for i in range(1, len(self.tb)):
            join_method = getattr(query, "join")
            value = False
            if join_type == "left join" or join_type == "right join":
                value = True
            # where conditions e.g [["states.id", "cities.id"],
            # ["amenities.id", "places.amenity_id"]].
            # e.g ["states.id". "cities.state_id"]
            condition = conditions[i - 1]
            left = getattr(tbl_clss[i-1], condition[0].split(".")[1])
            right = getattr(tbl_clss[i], condition[1].split(".")[1])
            query = join_method(tbl_clss[i], left == right, isouter=value)

        query = query.all()
        for row in query:
            row_data = []
            for each_table in row:
                if each_table:
                    for col in self.columns:
                        if col.split(".")[0] == each_table.__table__.name:
                            column_data = getattr(
                                each_table, col.split(".")[1])
                            row_data.append(column_data)
                else:
                    row_data.append("-")
            data.append(row_data)
        session.close()
        return data

    def del_data(self, column=None, value=None):
        """Deletes a row in the selected DB"""
        if not self.tables or not column or not value:
            print("Please at least a table, a column and a value")
            return
        self.column = column
        self.value = value
        self.tb = [self.mapped_db[tbl_cls]
                   for tbl_cls in self.mapped_db.keys()
                   if tbl_cls in self.tables]
        query = self.session.query(*self.tb)
        if query:
            self.__get_del(query)

    def __get_del(self, query):
        """function that carries out the deletion"""
        column = self.column.split(".")[1]
        if len(self.tb) == 1:
            query = query.filter_by(**{column: self.value}).all()
            if query:
                for row in query:
                    self.session.delete(row)
                    self.session.commit()
        else:
            k = 0  # choose the first value in self.tb
            for i in range(1, len(self.tb)):
                query = query.join(self.tb[i])
                if self.tb[i].__table__.name == self.column.split(".")[0]:
                    k = i  # if the table name matches the giving column name
            query = query.filter(getattr(
                self.tb[k], column) == self.value).all()
            if query:
                for rows in query:
                    for row in rows:
                        self.session.delete(row)
                        self.session.commit()
        self.session.close()

    def del_table_cols(self, columns=[]):
        """Delete column(s) of a selected Table(s)"""
        with self.engine.connect() as connection:
            for table in self.tables:
                for col in columns:
                    if table == col.split(".")[0]:
                        query = f"ALTER TABLE {table} \
                            DROP COLUMN {col.split('.')[-1]}"
                        connection.execute(text(query))
                        connection.commit()
        self.engine.dispose()

    @property
    def join_conditions(self):
        """
        Determines the join 'ON conditions' when dealing with multiple tables
        """
        amount_of_join = len(self.tables) * 2 - 2
        if amount_of_join == 1:
            # query.all()
            print("The len of tb is: ", len(self.tables))
            return None
        conditions = []
        for i in range(1, len(self.tables)):
            col1 = self.table_headers(self.tables[i-1], None)
            col2 = self.table_headers(self.tables[i], None)
            conditions.append([col1, col2])
        return conditions
