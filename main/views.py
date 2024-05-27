from django.http import HttpResponse
from django.shortcuts import render

from .models import Player, Tournament


def hi(request):
    return HttpResponse("<h1>HI</h1>")  # Create your views here.


def show_players(request):
    all_players = Player.objects.all()
    return HttpResponse(all_players)


def show_tournaments(request):
    all_tournaments = Tournament.objects.all()
    return HttpResponse(all_tournaments)


def create_tournament(request):
    if request.method == "POST":
        tournament_name = request.POST.get("tournament_name")
        player_name = request.POST.get("player_name")
        if tournament_name is not None:
            new_tournament = Tournament.create_new_tournament(name=tournament_name)
            return HttpResponse(
                f"<h1> Tournament name is {new_tournament.name}"
                '<form method="POST"> Player Name: <input name="player_name">'
            )
        else:
            return HttpResponse(
                f"<h1> Player name is {player_name}"
                '<form method="POST"> Player Name: <input name="player_name">'
            )

    else:
        return HttpResponse(
            "<h1>Hi! Create your tournament here</h1>"
            '<form method="POST"> Tournament Name: <input name="tournament_name">'
        )
