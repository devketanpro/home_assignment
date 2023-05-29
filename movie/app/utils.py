from datetime import datetime

from .config.db import db
from .models import Movie


def create_movie_record(movies):
    try:
        for movie in movies:
            movie_id = movie.get("movie", {}).get("value")
            imdb_id = movie.get("imdbId", {}).get("value")
            release_date = datetime.strptime(
                movie.get("releaseDate", {}).get("value"), "%Y-%m-%dT%H:%M:%SZ"
            ).date()
            movie_name = movie.get("movieLabel", {}).get("value")
            if not db.session.query(Movie).filter_by(imdb_id=imdb_id, movie=movie_id, release_date=release_date,
                                                     movie_name=movie_name).first():
                movie = Movie(movie=movie_id, movie_name=movie_name, imdb_id=imdb_id, release_date=release_date)
                db.session.add(movie)
                db.session.commit()

        return True
    except Exception as ex:
        return False
