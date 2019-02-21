from flask import Blueprint

bp = Blueprint('api',__name__)

from srv.api import users, errors, tokens