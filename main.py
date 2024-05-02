#!/usr/bin/env

from app.v1.filters import Filter
from app.v1.database import Database, CreateClassTable
from app.v1.user import User

# obj = Filter(2, "hbnb_dev_db")
# obj.update_data("cities", "cities.id", "Chicago")
x = User()
# x.addUser({
#             "mariadb": ["hbnb", "porche"],
#             "postgresql": ["parche"]
#         })
x.delUser(4)
