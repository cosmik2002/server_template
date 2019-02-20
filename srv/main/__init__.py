from flask import Blueprint

bp = Blueprint('main', __name__)

from srv.main import routes