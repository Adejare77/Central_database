# #!/usr/bin/env python


# class Join:
#     def __init__(self, classes) -> None:
#         pass


    def __join_method(self, join_type, tb) -> list:
        query = self.session.query(*self.tb)  # innerjoin
        query = self.session.query(*self.tb)

        list_dict = []
        for i in range(1, len(self.tb)):
            key1 = self.tb[i-1].name
            val1 = self.table_headers(self.tb[i-1].__table__.name)
            key2 = self.tb[i].name
            val2 = self.table_headers(self.tb[i].__table__.name)
            list_dict.append({key1: val1, key2: val2})
        return list_dict

        # self.tb = [self.mapped_db[tb] for tb in self.tables]
        # all_tbl_headers = [self.mapped_db[tb] for tb in self.tables]
