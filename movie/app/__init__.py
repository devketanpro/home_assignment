from flask_appbuilder import AppBuilder

from .config.app import app
from .config.db import db
from .models import *
from .views import FetchRecord, MovieView

appbuilder = AppBuilder(app, db.session)
appbuilder.add_view(FetchRecord, "Fetch Movies", category="Movie detail")
appbuilder.add_view(
    MovieView, "List Groups", category="Movie detail list", href="/movieview/list/"
)
