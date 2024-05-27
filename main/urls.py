from django.urls import path
from .views import hi, show_players, create_tournament, show_tournaments

urlpatterns = [
    path("hi/", hi),
    path("showplayers/", show_players),
    path("showtournaments/", show_tournaments),
    path("create-tournament/", create_tournament),
]
