#!/usr/bin/python3

from app.database import Database
from flask import redirect, request, render_template, url_for, session
from app.database import CreateClassTable
from app.filters import Filter
from app import app

# def get_db(username):
#     user = Database(username)
#     info = {username: user.get_db_list}
#     return info

# @central_db.route("/db_list/")
# def database_list():
#     db_list = Database(session.get("username")).db_list
#     # session["Databases"] = db_list
#     return render_template('radio.html', data=db_list, route="/db_selection/logic",
#                            name="database")

@app.route("/db_selection/logic/", methods=['POST'])
def query_del():
    value = request.form.get("action")
    selected_db = request.form.get("database")
    if value == "query":
        user_info = session.get("username")
        if selected_db not in user_info:
            user_info.append(selected_db)
        return redirect("/user/db_selection")
    else:
        user_info = session.get("username")
        if selected_db not in user_info:
            user_info.append(selected_db)
        inst = CreateClassTable(*user_info)
        inst.del_database
        session.get("username").remove(selected_db)
        return redirect("/db_list/")

@app.route("/user/db_selection", methods=['GET'])
def current_db():
    selected_db = request.form.get("database")
    table_list = CreateClassTable(*session.get("username")).get_tb_list
    return render_template('checkbox.html', data=table_list, route="/user/database/tables",
                           name="selected_tb")

@app.route("/user/database/tables", methods=['POST'])
def tables():
    if request.method == 'POST':
        selected_table = request.form.getlist("selected_tb")
    user_info = session.get("username")
    if selected_table not in user_info:
        user_info.append(selected_table)
    inst = Filter(*user_info)
    all_inst_headers = inst.table_headers()
    return render_template('checkbox.html', data=all_inst_headers, route="/user/database/tables/query",
                           name="columns")

@app.route("/user/database/tables/query", methods=['POST'])
def query():
    columns = request.form.getlist("columns")
    user_info = session.get('username')
    inst = Filter(*user_info)
    inst.table_headers(columns)
    obj = inst.all_rows()
    return render_template('data.html', headers=columns, data=obj)

# print("*********************************************")
# print(app.url_map)
# print("*********************************************")
