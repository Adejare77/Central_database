#!/usr/bin/python3

from app.v1.database import Database
from app.v1.views import central_db
from flask import session, redirect, request, render_template
from uuid import uuid4


def get_db(username):
    user = Database(username)
    info = {username: user.get_db_list}
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
        if username in user_info.keys():
            session["username"] = [username]
            # session["database"] = database
            return redirect("/db_list/{}".format(username))
        return redirect("/")
    return render_template("login.html")
