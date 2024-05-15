#!/usr/bin/env
from os import system, getenv

# from app.filters import Filter
# from app.database import Database, CreateClassTable

# obj = Filter(11, "hbnb_dev_db", ["amenities", "cities"], ["amenities.name", "cities.name"])
# print(obj.tbl_headers)
# print("----------------------------------------")
# print(obj.all_rows("rightjoin", [["amenities.name", "cities.name"], ["cities.name", "states.name"]]))
# # obj = Filter(11, "hbnb_dev_db", ["cities", "states"])
# # print(obj.join_groups)
# # print("==================================")
# # print(obj.all_rows("outerjoin", [["cities.state_id", "states.id"]]))

mypasswd = "legolas"


system('echo {} | sudo -S apt-get install nginx'.format(mypasswd))
