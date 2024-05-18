#!/usr/bin/python3
""" module contains routing specifications for the query pages"""

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
    """
    Handles GET requests for viewing a list of tables in a specific database
    """
    session['database'] = db
    table_list = CreateClassTable(current_user.id, db).get_tb_list
    return render_template('checkbox.html',
                           data=table_list, name="table",
                           route="/user/database/table/tbls_options",
                           description="Please select TABLE(s) to be Displayed")


@app.route('/user/database/table/tbls_options', methods=['POST'])
@login_required
def table_options():
    """handles control flow for POST requests for performing actions on
    selected tables from the table list.
    """
    option = request.form.get("action")
    selected_tables = request.form.getlist('table')
    if option == "Query":
        return redirect(url_for('table_columns', tables=selected_tables))
    CreateClassTable(current_user.id,
                     session.get('database')).del_table(selected_tables)
    return redirect(url_for('table_lists', db=session.get('database')))


@app.route('/user/database/table_cols/<tables>', methods=['GET'])
@login_required
def table_columns(tables):
    """returns list of columns in selected tables"""
    if not session.get('database'):
        return redirect(url_for('index'))
    tables = eval(tables)  # if received from url_for, always use eval
    session['tables'] = tables
    inst = Filter(current_user.id, session.get('database'), tables)
    headers = inst.table_headers(tables, None)
    return render_template('checkbox.html', data=headers,
                           route="/user/database/table_cols/cols_options",
                           name="columns",
                           description="Please select COLUMNS to display")


@app.route('/user/database/table_cols/cols_options', methods=['POST'])
@login_required
def columns_options():
    """determines what action will be done on selected columns"""
    if not session.get('tables'):
        return redirect(url_for('index'))
    option = request.form.get("action")
    columns = request.form.getlist('columns')
    session['columns'] = columns
    if option == "Query":
        return redirect(url_for('table_query', columns=columns))
    Filter(current_user.id, session.get('database'),
           session.get('tables')).del_table_cols(columns)
    return redirect(url_for('table_columns', tables=session.get('tables')))


@app.route("/user/database/query/<columns>", methods=['GET', 'POST'])
@login_required
def table_query(columns):
    """ route handles GET requests for executing and displaying
    a query on the selected columns."""
    if not session.get('tables'):
        return redirect(url_for('index'))

    if len(session['tables']) == 1:
        inst = Filter(current_user.id, session.get('database'),
                      session['tables'], eval(columns))
        headers = inst.table_headers(session['tables'],
                                     session.get('columns'))
        return render_template('data.html', headers=headers,
                               data=inst.all_rows(),
                               back=session.get('database'))

    if request.method == 'GET':
        join_types = ["join", "left join", "right join"]
        if len(session['tables']) > 2:
            join_types.remove('right join')
        # session['columns'] = columns
        inst = Filter(current_user.id, session.get('database'),
                      session['tables'], eval(columns))
        return render_template('radio.html', join_types=join_types,
                               data=inst.join_conditions,
                               route="/user/database/query/" + columns)

    join_type = request.form.get('join')
    tables = session['tables']
    if join_type == "right join":
        tables = session['tables']
        tables = list([tables[1], tables[0]])

    # inst = Filter(current_user.id, session.get('database'),
    #               session['tables'], (eval(session.get('columns'))))
    inst = Filter(current_user.id, session.get('database'),
                  tables, eval(columns))
    # headers = inst.table_headers(tables,
    #                              eval(session.get('columns')))
    headers = inst.table_headers(tables,
                                 eval(columns))
    condition_keys = eval(request.form.get('action'))  # eval converts to list
    conditions = []
    for items in condition_keys:
        group_conditions = []
        for element in items:
            group_conditions.append(request.form.get(element))
        conditions.append(group_conditions)

    if join_type == "right join":
        conditions = [list([conditions[0][1], conditions[0][0]])]

    return render_template('data.html', headers=headers,
                           data=inst.all_rows(join_type, conditions),
                           back=session.get('database'))

# [ ]: Flask Route for AJAX Requests
# @app.route('/user/database/dynamic_tblheaders', methods=['POST'])
# def dynamic_data():
#     """ flask route to handle AJAX requests"""
    # recieves the list of selected tables sent from AJAX
#     selected_tables = (request.json)['selected_tables']
    # inst = Filter(current_user.id, session.get('database'),
    #               selected_tables)
    # return jsonify({"headers":inst.table_headers,
    #                 "route":"/user/database/cols_options"})
