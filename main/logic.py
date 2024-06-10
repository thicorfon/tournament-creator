from math import ceil
from random import shuffle


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
