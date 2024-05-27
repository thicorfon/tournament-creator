from django.urls import path
from .views import hi, show_players, create_tournament

urlpatterns = [
    path("hi/", hi),
    path("showplayers/", show_players),
    path("create-tournament/", create_tournament),
]
