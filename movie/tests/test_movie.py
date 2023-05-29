import os
import sys
from datetime import date
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
sys.path.append(os.path.abspath(".."))
from movie.app.models import Movie
from movie.app.views import FetchRecord, MovieView


class MovieViewTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["TESTING"] = True
        self.app.config.from_object("movie.config")
        self.db = SQLA(self.app)
        self.db.create_all()
        self.appbuilder = AppBuilder(self.app, self.db.session)
        self.client = self.app.test_client()
        movie = Movie(movie_name="Test Movie", imdb_id="123456", release_date=date.today(), movie="dklfjsd")
        self.db.session.add(movie)
        self.db.session.commit()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_movie_view_list_columns(self):
        with self.client:
            movie_list_view = MovieView()
            self.appbuilder.add_view(movie_list_view, "List Groups", category="Movie detail list",
                                     href="/list_groups/movieview/list/")
            response = self.client.get("/movieview/list/")
            data = response.get_data(as_text=True)
            self.assertIn("You should be redirected automatically to the target URL", data)


class FetchRecordTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, template_folder=os.getcwd() + '/app/config/templates')
        self.app.config["TESTING"] = True
        self.app.config.from_object("movie.config")
        self.db = SQLA(self.app)
        self.db.create_all()
        self.appbuilder = AppBuilder(self.app, self.db.session)
        self.client = self.app.test_client()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    @patch("movie.app.views.requests.get")
    @patch("movie.app.views.create_movie_record")
    def test_fetch_movies_success(self, mock_create_movie_record, mock_requests_get):
        response_data = {
            "results": {
                "bindings": [
                    {
                        "movie": {"value": "Movie 1"},
                        "movieLabel": {"value": "Movie Label 1"},
                        "imdbId": {"value": "123456"},
                        "releaseDate": {"value": "2023-01-01"},
                    },
                    {
                        "movie": {"value": "Movie 2"},
                        "movieLabel": {"value": "Movie Label 2"},
                        "imdbId": {"value": "7890"},
                        "releaseDate": {"value": "2023-02-01"},
                    },
                ]
            }

        }
        mock_requests_get.return_value = MagicMock(status_code=200, json=lambda: response_data)
        mock_create_movie_record.return_value = True

        with self.app.app_context():
            fetch_record_view = FetchRecord()
            self.appbuilder.add_view(fetch_record_view, "Fetch Movies", category="Movie detail")
            response = self.client.get("/fetchrecord/fetch_record/")
            self.assertIn("Data inserted into the database successfully.", response.data.decode("utf-8"))
            mock_create_movie_record.assert_called_once_with(response_data["results"]["bindings"])

    @patch("movie.app.views.requests.get")
    @patch("movie.app.views.create_movie_record")
    def test_fetch_movies_error(self, mock_create_movie_record, mock_requests_get):
        mock_requests_get.return_value = MagicMock(status_code=500)
        with self.app.app_context():
            fetch_record_view = FetchRecord()
            self.appbuilder.add_view(fetch_record_view, "Fetch Movies", category="Movie detail")
            response = self.client.get("/fetchrecord/fetch_record/")
            self.assertEqual(response.status_code, 200)
            self.assertIn("Error occurred during data retrieval.", response.data.decode("utf-8"))
            mock_create_movie_record.assert_not_called()


if __name__ == "__main__":
    unittest.main()
