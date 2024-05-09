#!/usr/bin/python3
""" module contains routing spwcifications for the query pages"""
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
    """Handles GET requests for viewing a list of tables in a specific database"""
    session['database'] = db
    table_list = CreateClassTable(current_user.id, db).get_tb_list
    return render_template('checkbox.html', data=table_list, route="/user/database/tbls_options",
                        name="table")

@app.route('/user/database/tbls_options', methods=['POST'])
@login_required
def table_options():
    """handles control flow for POST requests for performing actions on
    selected tables from the table list.
    """
    option = request.form.get("action")
    selected_tables = request.form.getlist('table')
    if option == "Query":
        return redirect(url_for('table_columns', tables=selected_tables))
    CreateClassTable(current_user.id, session.get('database')).del_table(selected_tables)
    return redirect(url_for('table_lists', db=session.get('database')))

# [ ]: Route to replace with AJAx handler 
@app.route('/user/database/<tables>', methods=['GET'])
@login_required
def table_columns(tables):
    """returns list of columns in selected tables"""
    tables = eval(tables)  # if received from url_for, always use eval
    session['tables'] = tables
    inst = Filter(current_user.id, session.get('database'), tables)
    return render_template('checkbox.html', data=inst.table_headers, route="/user/database/cols_options",
                           name="columns")

@app.route('/user/database/cols_options', methods=['POST'])
@login_required
def columns_options():
    option = request.form.get("action")
    columns = request.form.getlist('columns')
    if option == "Query":
        return redirect(url_for('table_query', columns=columns))
    Filter(current_user.id, session.get('database'), session.get('tables')).del_table_cols(columns)
    return redirect(url_for('table_columns', tables=session.get('tables')))

@app.route("/user/database/query/<columns>", methods=['GET'])
@login_required
def table_query(columns):
    """ route handles GET requests for executing and displaying a query  on the selected columns."""
    columns = eval(columns)
    inst = Filter(current_user.id, session.get('database'),
                  session['tables'], columns)
    return render_template('data.html', headers=inst.table_headers, data=inst.all_rows())

# [ ]: Flask Route for AJAX Requests
# @app.route('/user/database/dynamic_tblheaders', methods=['POST'])
# def dynamic_data():
#     """ flask route to handle AJAX requests"""
#     selected_tables = (request.json)['selected_tables'] # recieves the list of selected tables sent from AJAX
#     inst = Filter(current_user.id, session.get('database'), selected_tables)
#     return jsonify({"headers":inst.table_headers, "route":"/user/database/cols_options"})




# @app.route("/user/database/<del_tables>", methods=['GET'])
# @login_required
# def del_table(tables):
#     inst = CreateClassTable(current_user.id, session.get('database')).del_table(tables)
#     # return render_template('checkbox.html', data=all_inst_headers, route="/user/database/option",
#     #                        name="columns")
#     return redirect('/user/database/db')

