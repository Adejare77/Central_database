#!/usr/bin/python3

from app.database import Database
from flask import redirect, request, render_template, url_for, session
from app.database import CreateClassTable
from app.filters import Filter
from app import app

from flask_login import current_user
from flask_login import login_required
from flask import request


@app.route("/user/database/<string:db>/", methods=['GET'])
@login_required
def table_lists(db):
        session['database'] = db
        table_list = CreateClassTable(current_user.id, db).get_tb_list
        return render_template('checkbox.html', data=table_list, route="/user/database/tables",
                           name="table")

@app.route("/user/database/tables", methods=['POST'])
@login_required
def tables():
    selected_table = request.form.getlist("table")
    session['tables'] = selected_table
    # user_info = session.get("username")
    # if selected_table not in user_info:
    #     user_info.append(selected_table)
    inst = Filter(current_user.id, session.get('database'), selected_table)
    all_inst_headers = inst.table_headers
    return render_template('checkbox.html', data=all_inst_headers, route="/user/database/tables/query",
                           name="columns")

@app.route("/user/database/tables/query", methods=['POST'])
def query():
    columns = request.form.getlist("columns")
    user_info = session.get('username')
    inst = Filter(current_user.id, session.get('database'),
                  session.get('tables'), columns)
    return render_template('data.html', headers=inst.table_headers, data=inst.all_rows())
