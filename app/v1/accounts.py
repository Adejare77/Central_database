# #!/usr/bin/env python3

# from os import getenv
# from app.v1.central_db_tables import Primary_owner, Other_users
# from app.v1.database import Database, CreateClassTable
# from sqlalchemy import create_engine, update
# from sqlalchemy.orm import sessionmaker

# class Account(CreateClassTable):
#     def __init__(self, id, db, tables, columns=None) -> None:
#         super().__init__(id, db)
#         if type(tables) == str:
#             tables = list([tables])
#         self.tables = tables
#         self.columns = columns
#         self.db = db
#         self.get_fmt_db = db

#     @property
#     def other_users(self):
#         users = self.session.query(Other_users.username).filter_by(owner=self.user)
#         users = [user for user in users]
#         print(users)

#     # def get_user_permissions(self, db=None, other_username=None) -> list:
#     #     if self.is_owner is not Primary_owner or not other_username or not db:
#     #         return
#     #     permissions = Database(self.user).session.query(Other_users.permissions).filter_by(username=other_username).one()
#     #     operations = permissions[0][db]
#     #     return operations

#     # def update_permissions(self, db, other_username, permissions):
#     #     if self.is_owner != Primary_owner:
#     #         return
#     #     if type(permissions) == str:
#     #         permissions = list([permissions])
#     #     all_permissions = ["READ", "CREATE", "DELETE", "UPDATE"]
#     #     if not set(permissions).issubset(all_permissions):
#     #         print("Permission can only be one or a list of this:")
#     #         print(all_permissions)

#         # # query_perm = Database(self.user).session.query(Other_users.permissions).filter_by(username=other_username).one()
#         # return
#         # url = Database.url
#         # engine = create_engine(url, pool_pre_ping=True)
#         # session = sessionmaker(bind=engine)()
#         # print("------------------------------------")
#         # query_perm = session.query(Other_users.permissions).filter_by(username=other_username).one()
#         # query_perm.permissions[db] = permissions
#         # print(query_perm[0])
#         # print(type(query_perm))
#         # print(type(query_perm[0]))
#         # query = session.query(Other_users.permissions).filter_by(username=other_username).update(query_perm[0])
#         # session.commit()
#         # print("------------------------------------")
#         # permissions_dict = query_perm[0]
#         # permissions_dict[0][db] = permissions
#         # print(permissions_dict[0])
#         # query_perm.update(permissions_dict[0])
#         # return
#         # print("------------------------------------")
#         # print("=====================================")
#         # print(permissions_dict)

#         # # Update the permissions for the specific database
#         # permissions_dict[self.db] = permissions
#         # # Commit the changes
#         # session.commit()
#         # print("------------------------------")
#         # # print(query_perm[0][self.db])
#         # # query_perm[0][self.db] = permissions
#         # # session.commit()
#         # print("------------------------------")

#     @property
#     def permissions(self) -> list:
#         operations = ["READ", "DELETE"]
#         if self.is_owner == Primary_owner:
#             return operations
#         query_perm = Database(self.user).session.query(Other_users.permissions).filter_by(username=self.user).one()
#         perm_op = [perm for perm in operations if perm in query_perm[0][self.db]]
#         return perm_op
