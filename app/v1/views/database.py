#!/usr/bin/python3

from app.v1.database import Database
from app.v1.views import central_db
from flask import redirect, request, render_template, url_for, session
from app.v1.database import CreateClassTable
from app.v1.accounts import Account
from app.v1.filters import Filter

def get_db(username):
    user = Database(username)
    info = {username: user.get_db_list}
    return info

@central_db.route("/db_list/<username>")
def database_list(username):
    db_list = list(get_db(username).values())[0]
    return render_template('radio.html', data=db_list)

@central_db.route("/selected_db", methods=['POST'])
def current_db():
    selected_db = request.form.get("db")
    user_info = session.get("username")
    user_info.append(selected_db)
    table_list = CreateClassTable(*user_info).get_tb_list
    return render_template('checkbox.html', data=table_list)

@central_db.route("/user/database/tables", methods=['POST'])
def tables():
    if request.method == 'POST':
        selected_table = request.form.getlist("selected_tb")
    user_info = session.get("username")
    user_info.append(selected_table)
    available_query = Account(*user_info).permissions
    return render_template('operations.html', data=available_query)

@central_db.route("/query_db", methods=['POST'])
def query():
    query = request.form.get("operations")
    user_info = session.get('username')
    inst = Filter(*user_info)
    if query == "READ":
        headers = inst.table_headers()
        data =  inst.all_rows()
        return render_template('data.html', headers=headers, data=data)
    elif query == "DELETE":
        inst.del_data()
        return "row deleted"
