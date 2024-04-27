#!/usr/bin/env

from app.v1.rbac import Filter
from app.v1.user_db import CreateClassTable, Database
from app.v1.accounts import Account

# obj = Database("Rashisky")
# print(obj.get_db_list)

# obj.get_fmt_db = "hbnb_dev_db"
# print(obj.get_fmt_db)

# user = CreateClassTable("Rashisky", "hbnb_dev_db")
# # print(user.get_tb_list)
# print(user.get_tb_columns("states"))

user = Filter("Rashisky", "hbnb_dev_db")
user.all(["cities", "states"], ["states.id"])
