#!/usr/bin/env python3

from flask import Blueprint
from flask_session import Session


central_db = Blueprint("central_db", __name__)
