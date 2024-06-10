from django.http import HttpResponse
from django.shortcuts import render

from .models import Player, Tournament, TournamentStatus, Round, Match
from .front_logic import build_player_list, build_round_summary
from .logic import calculate_random_ranking, calculate_round_matches


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
        if player_name is None:
            new_tournament = Tournament.create_new_tournament(name=tournament_name)
            new_tournament.save()
            return HttpResponse(
                f"<h1> Tournament name is {new_tournament.name}"
                '<form method="POST"> '
                'Player Name: <input name="player_name">'
                f'<input name="tournament_name" type="hidden" value="{new_tournament.name}">'
                "</form>"
            )
        else:
            new_player = Player.create_new_player(name=player_name)
            new_player.save()
            current_tournament = Tournament.objects.get(name=tournament_name)
            current_tournament.players.add(new_player)
            current_tournament.save()
            player_list = current_tournament.players.all()
            return HttpResponse(
                f"<h1> Tournament name is {tournament_name}"
                '<form method="POST"> '
                'Player Name: <input name="player_name">'
                f'<input name="tournament_name" type="hidden" value="{current_tournament.name}">'
                '<input type="submit" value="Add Player">'
                "</form>"
                f'<form action=/tournament/{current_tournament.name} method="GET">'
                '<input type="submit" value="Create Tournament">'
                "</form>" + "\n\n" + build_player_list(player_list)
            )

    else:
        return HttpResponse(
            "<h1>Hi! Create your tournament here</h1>"
            '<form method="POST"> Tournament Name: <input name="tournament_name">'
        )


def tournament_summary(request, name):
    current_tournament = Tournament.objects.get(name=name)
    if request.method == "POST":
        player_name = request.POST.get("player_name")
        update_results = request.POST.get("update_results")
        finish_round = request.POST.get("finish_round")

        if player_name is not None:
            new_player = Player.create_new_player(name=player_name)
            new_player.save()
            current_tournament.players.add(new_player)
            current_tournament.save()

        if update_results is not None:
            current_round = Round.objects.filter(tournament=current_tournament).get(
                number=current_tournament.current_round
            )
            current_matches = Match.objects.filter(round=current_round).all()
            for match in current_matches:
                for player in match.result:
                    match.result[player] = int(
                        request.POST.get(str(match.number) + player)
                    )
                    match.save()

        if finish_round is not None:
            current_tournament.status = TournamentStatus.WAITING_ROUND
            current_tournament.save()

    response = f"<h1> Tournament: {current_tournament.name}</h1>"
    response += build_player_list(current_tournament.players.all())
    response += f"<h2><b>Tournament Status:</b> {current_tournament.status} <br></h2>"
    response += (
        f"<h2><b>Current Round:</b> {current_tournament.current_round} <br></h2>"
    )
    if current_tournament.status == TournamentStatus.ACTIVE_ROUND:
        current_round = Round.objects.filter(tournament=current_tournament).get(
            number=current_tournament.current_round
        )
        response += build_round_summary(Match.objects.filter(round=current_round).all())

    if (
        current_tournament.status != TournamentStatus.ACTIVE_ROUND
        and current_tournament.status != TournamentStatus.FINISHED
    ):
        response += (
            f'<form action=/tournament/{current_tournament.name}/launch-round method="GET">'
            f'<input type="submit" value="Launch New Round">'
            f"</form>"
        )
    response += (
        f"<form method='POST'>"
        f'Player Name: <input name="player_name">'
        f'<input type="submit" value="Add Player">'
        f"</form>"
    )
    return HttpResponse(response)


def launch_round(request, name):
    current_tournament = Tournament.objects.get(name=name)
    if (
        current_tournament.status == TournamentStatus.STARTED
        or current_tournament.status == TournamentStatus.WAITING_ROUND
    ):
        all_rounds = Round.objects.filter(tournament=current_tournament)
        all_matches = []
        for current_round in all_rounds:
            all_matches.extend(Match.objects.filter(round=current_round))
        players = current_tournament.players.all()
        randomized_ordered_rank = calculate_random_ranking(
            all_matches, [x.name for x in players]
        )
        round_matches = calculate_round_matches(
            current_tournament.desired_table_size, randomized_ordered_rank
        )
        current_tournament.current_round = current_tournament.current_round + 1
        current_tournament.status = TournamentStatus.ACTIVE_ROUND
        current_tournament.save()
        new_round = Round.create_new_round(
            number=current_tournament.current_round,
            players=players,
            tournament=current_tournament,
        )
        new_round.save()
        match_number = 1
        for match in round_matches:
            new_match = Match.create_new_match(
                players=[Player.objects.get(name=x) for x in match],
                round=new_round,
                number=match_number,
            )
            new_match.save()
            match_number += 1

    return tournament_summary(request, name)
