from django.urls import path

from movies.views import MovieIdView, MovieView

urlpatterns = [
    path("movies/<int:movie_id>/", MovieIdView.as_view()),
    path("movies/", MovieView.as_view())
]