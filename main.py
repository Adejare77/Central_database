#!/usr/bin/env

from app.filters import Filter
from app.database import Database, CreateClassTable
from app.user import User

# obj = Filter(2, "hbnb_dev_db")
# obj.update_data("cities", "cities.id", "Chicago")
x = User().addUser()
# x.addUser({
#             "mariadb": ["hbnb", "porche"],
#             "postgresql": ["parche"]
#         })
# x.delUser(4)
