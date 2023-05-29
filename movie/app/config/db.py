from flask_appbuilder import SQLA

from .app import app

db = SQLA(app)
