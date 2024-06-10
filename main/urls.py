from django.urls import path
from .views import (
    hi,
    show_players,
    create_tournament,
    show_tournaments,
    tournament_summary,
    launch_round,
)

urlpatterns = [
    path("hi/", hi),
    path("show-players/", show_players),
    path("show-tournaments/", show_tournaments),
    path("create-tournament/", create_tournament),
    path("tournament/<str:name>", tournament_summary),
    path("tournament/<str:name>/launch-round", launch_round),
]
