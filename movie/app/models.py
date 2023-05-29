from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

"""
You can use the extra Flask-AppBuilder fields and Mixin's
AuditMixin will add automatic timestamp of created and modified by who
"""


class Movie(Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    movie = Column(String(255), nullable=False)
    movie_name = Column(String(255), nullable=False)
    imdb_id = Column(String(255), nullable=False)
    release_date = Column(Date, nullable=False)
