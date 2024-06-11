from math import ceil
from random import shuffle
from django.db.models import Q


def calculate_tiebreakers(not_ordered_rank, opponents_list):
    tiebreakers = {}
    for player_name in list(not_ordered_rank.keys()):
        player_opponents = opponents_list[player_name]
        numerator = 0
        denominator = 0
        for opponent in player_opponents:
            numerator += not_ordered_rank[opponent]
            denominator += 1
        if denominator != 0:
            tiebreakers[player_name] = numerator / denominator
        else:
            tiebreakers[player_name] = 0
    return tiebreakers


def calculate_ranking_with_tiebreakers(list_of_matches, player_names):
    not_ordered_rank = {}
    opponents_list = {}
    for player_name in player_names:
        opponents_list[player_name] = []
    for match in list_of_matches:
        for player in match.players.all():
            aux = not_ordered_rank.get(player.name, None)
            opponents = match.players.filter(~Q(name=player.name)).all()
            opponents_list[player.name].extend([x.name for x in opponents])
            if aux is None:
                not_ordered_rank[player.name] = match.result[player.name]
            else:
                not_ordered_rank[player.name] += match.result[player.name]
    for player_name in player_names:
        aux = not_ordered_rank.get(player_name, None)
        if aux is None:
            not_ordered_rank[player_name] = 0
    tiebreakers = calculate_tiebreakers(not_ordered_rank, opponents_list)
    second_tiebreakers = calculate_tiebreakers(tiebreakers, opponents_list)
    final_not_ordered_rank = []
    for player_name in list(not_ordered_rank.keys()):
        final_not_ordered_rank.append(
            (
                player_name,
                not_ordered_rank[player_name],
                tiebreakers[player_name],
                second_tiebreakers[player_name],
            )
        )
    return sorted(
        final_not_ordered_rank, key=lambda x: (x[1], x[2], x[3]), reverse=True
    )


def randomize_and_order_rank(not_ordered_rank):
    randomized_rank = []
    keys_list = list(not_ordered_rank.keys())
    shuffle(keys_list)
    for key in keys_list:
        randomized_rank.append((key, not_ordered_rank[key]))
    return sorted(randomized_rank, key=lambda x: x[1], reverse=True)


def calculate_random_ranking(list_of_matches, player_names):
    not_ordered_rank = {}
    for match in list_of_matches:
        for player in match.players.all():
            aux = not_ordered_rank.get(player.name, None)
            if aux is None:
                not_ordered_rank[player.name] = match.result[player.name]
            else:
                not_ordered_rank[player.name] += match.result[player.name]
    for player_name in player_names:
        aux = not_ordered_rank.get(player_name, None)
        if aux is None:
            not_ordered_rank[player_name] = 0
    return randomize_and_order_rank(not_ordered_rank)


def calculate_round_matches(desired_table_number, ranking_with_active_players):
    aux_ranking = ranking_with_active_players
    round_matches = []
    number_of_players = len(ranking_with_active_players)
    number_of_tables = ceil(1.0 * number_of_players / desired_table_number)
    number_of_tables_with_reduced_players = (
        number_of_tables * desired_table_number - number_of_players
    )
    number_of_full_tables = number_of_tables - number_of_tables_with_reduced_players
    for i in range(number_of_full_tables):
        current_table = []
        for j in range(desired_table_number):
            current_player = aux_ranking.pop(0)[0]
            current_table.append(current_player)
        round_matches.append(current_table)
    for i in range(number_of_tables_with_reduced_players):
        current_table = []
        for j in range(desired_table_number - 1):
            current_player = aux_ranking.pop(0)[0]
            current_table.append(current_player)
        round_matches.append(current_table)
    return round_matches
