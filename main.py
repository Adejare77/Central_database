#!/usr/bin/env

from app.v1.rbac import Filter, Create_Class

x = Filter("Ayokunnu", "hbnb_dev_db")
# x = Create_Class("hbnb_dev_db")

print(x.header(["cities"]))
x.all("cities")

# u = []
# l = [1, 2, 3, 4]

# u.extend(l)
# print(u)
