#!/usr/bin/python3

from app.database import Database
from app.v1.views import central_db
from flask import session, redirect, request, render_template
import json


def get_db(username):
    # db_list = Database(username).db_list
    db_list = Database(username)
    if not db_list.db_list:
        return None
    info = {username: db_list}
    # session["Database"] = f"{db_list.__dict__}"
    return info

@central_db.route("/")
def index():
    # selects a user and a database of exists
    if not session.get("username"):
        return redirect("/login")
    return render_template('login.html')

@central_db.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        user_info = get_db(username)
        x = session.get("Database")
        if not user_info:
            return "Username Not Found"
        elif username in user_info.keys():
            session["username"] = [username]
            return redirect("/db_list")
        return redirect("/")
    return render_template("login.html")
