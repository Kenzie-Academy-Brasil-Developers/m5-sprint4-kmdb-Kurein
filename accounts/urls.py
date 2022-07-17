from django.urls import path

from accounts.views import LoginView, UserView, UserGetView, UserIdView

urlpatterns = [
    path("users/<int:user_id>", UserIdView.as_view()),
    path("users/", UserGetView.as_view()),
    path("users/register/", UserView.as_view()),
    path("users/login/", LoginView.as_view()),
]