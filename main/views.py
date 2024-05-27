from django.http import HttpResponse
from django.shortcuts import render

from .models import Player


def hi(request):
    return HttpResponse("<h1>HI</h1>")  # Create your views here.


def show_players(request):
    all_players = Player.objects.all()
    return HttpResponse(all_players)


def create_tournament(request):
    if request.method == "POST":
        tournament_name = request.POST.get("tournament_name")
        player_name = request.POST.get("player_name")
        if tournament_name is not None:

            return HttpResponse(
                f"<h1> Tournament name is {tournament_name}"
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
