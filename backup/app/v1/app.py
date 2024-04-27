#!/usr/bin/python3

from flask import Flask, session, redirect, request, render_template
from flask_session import Session
from app.v1 import my_session
from app.v1.central_db_tables import Primary_owner, Other_users


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_secret_key_here'
Session(app)


def get_db():
    rows = my_session.query(Primary_owner.username,
                           Primary_owner.db_list).all()
    users = {}
    for row in rows:
        users[row.username] = row.db_list
    # print("============================")
    # print(users)
    # print("============================")
    return users


@app.route("/")
def index():
    # selects a user and a database of exists
    if not session.get("username"):
        return redirect("/login")
    # print("----------------------------")
    # print("INDEX CALLED")
    # print("----------------------------")
    return render_template('login.html')

@app.route("/login", methods=['GET','POST'])
def login():
    # print("----------------------------")
    # print("LOGIN CALLED")
    # print("----------------------------")
    if request.method == "POST":
        username = request.form.get("username")
        database = request.form.get("database")

        if username in get_db().keys():
            session["username"] = username
            session["database"] = database
            return redirect("/db_list")
        return redirect("/")
    # print("----------------------------")
    # print("REQUEST METHOD IS GET")
    # print("----------------------------")
    return render_template("login.html")

@app.route("/db_list")
def database_list():
    return "Hello There"

if __name__ == "__main__":
    app.run(debug=True)
