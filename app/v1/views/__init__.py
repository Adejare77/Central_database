#!/usr/bin/env python3

from flask import Flask, session, redirect, request, render_template, Blueprint
from flask_session import Session
from app.v1 import my_session
from app.v1.central_db_tables import Primary_owner, Other_users


central_db = Blueprint("central_db", __name__)
