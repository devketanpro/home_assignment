import requests
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Movie
from .utils import create_movie_record


class FetchRecord(BaseView):
    default_view = "fetch_movies"
    query = """SELECT ?movie ?movieLabel ?imdbId ?releaseDate WHERE {
        ?movie wdt:P31 wd:Q11424;  
               wdt:P577 ?releaseDate;  
               wdt:P345 ?imdbId;  
               FILTER (YEAR(?releaseDate) > 2013).
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }"""

    @expose("/fetch_record/")
    def fetch_movies(self):
        response = requests.get("https://query.wikidata.org/sparql", params={"format": "json", "query": self.query})
        if response.status_code == 200:
            movie_data = response.json().get("results").get("bindings")
            if create_movie_record(movie_data):
                return self.render_template(
                    "success_page.html",
                    context={
                        "message": "Data inserted into the database successfully."
                    },
                )
            return self.render_template(
                "error_page.html",
                context={"message": "Error occurred during data retrieval."},
            )
        return self.render_template(
            "error_page.html",
            context={"message": "Error occurred during data retrieval."},
        )


class MovieView(ModelView):
    datamodel = SQLAInterface(Movie)
    list_columns = ["movie", "movie_name", "imdb_id", "release_date"]
