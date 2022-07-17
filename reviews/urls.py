from django.urls import path

from reviews.views import ReviewView, ReviewGetView, ReviewIdView

urlpatterns = [
    path("movies/<int:movie_id>/reviews/", ReviewView.as_view()),
    path("reviews/<int:review_id>/", ReviewIdView.as_view()),
    path("reviews/", ReviewGetView.as_view())
]