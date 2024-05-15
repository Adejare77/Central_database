#!/usr/bin/python3

from app.database import Database
from flask import redirect, request, render_template, url_for, session
from app.database import CreateClassTable
from app.filters import Filter
from app import app
from flask_login import current_user
from flask_login import login_required
from flask import request
import json


@app.route("/user/database/<string:db>/", methods=['GET'])
@login_required
def table_lists(db):
    session['database'] = db
    table_list = CreateClassTable(current_user.id, db).get_tb_list
    return render_template('checkbox.html', data=table_list, route="/user/database/table/tbls_options",
                        name="table")

@app.route('/user/database/table/tbls_options', methods=['POST'])
@login_required
def table_options():
    option = request.form.get("action")
    selected_tables = request.form.getlist('table')
    if option == "Query":
        return redirect(url_for('table_columns', tables=selected_tables))
    CreateClassTable(current_user.id, session.get('database')).del_table(selected_tables)
    return redirect(url_for('table_lists', db=session.get('database')))

@app.route('/user/database/table_cols/<tables>', methods=['GET'])
@login_required
def table_columns(tables):
    if not session.get('database'):
        return redirect(url_for('index'))
    tables = eval(tables)  # if received from url_for, always use eval
    session['tables'] = tables
    inst = Filter(current_user.id, session.get('database'), tables)
    headers = inst.tbl_headers
    return render_template('checkbox.html', data=headers, route="/user/database/table_cols/cols_options",
                           name="columns")

@app.route('/user/database/table_cols/cols_options', methods=['POST'])
@login_required
def columns_options():
    if not session.get('tables'):
        return redirect(url_for('index'))
    option = request.form.get("action")
    columns = request.form.getlist('columns')
    if option == "Query":
        return redirect(url_for('table_query', columns=columns))
    Filter(current_user.id, session.get('database'), session.get('tables')).del_table_cols(columns)
    return redirect(url_for('table_columns', tables=session.get('tables')))

@app.route("/user/database/query/<columns>", methods=['GET', 'POST'])
@login_required
def table_query(columns):
    if not session.get('tables'):
        return redirect(url_for('index'))
    if request.method == 'GET' and len(session['tables']) > 1:
        join_types = ["join", "leftjoin", "rightjoin"]
        session['columns'] = str(columns)
        inst = Filter(current_user.id, session.get('database'),
                    session['tables'], eval(columns))
        return render_template('radio.html', join_types=join_types, data=inst.join_conditions, route="/user/database/query/" + columns)

    join_type = request.form.get('join')
    inst = Filter(current_user.id, session.get('database'),
                    session['tables'], (eval(session.get('columns'))))
    headers = inst.tbl_headers
    condition_keys = eval(request.form.get('action'))  # eval converts to list
    conditions = []
    for items in condition_keys:
        group_conditions = []
        for element in items:
            group_conditions.append(request.form.get(element))
        conditions.append(group_conditions)

    return render_template('data.html', headers=headers, data=inst.all_rows(join_type, conditions), back=session.get('database'))
