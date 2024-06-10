def build_player_list(player_list):
    component = "<h2>Players: </h2><ul>"
    for player in player_list:
        component += "\n"
        component += f"<li>{player.name}</li>"
    component += "</ul>"
    return component


def build_round_summary(round_matches, report=True):
    component = ""
    if report:
        component += '<form method="POST">'
    component += "<ul>"
    for match in round_matches:
        players_names = [x.name for x in match.players.all()]
        component += f"<li>Table {match.number}:</li><ul>"
        for name in players_names:
            component += f"<li>{name}"
            if report:
                component += f"<input name={str(match.number) + name} value={match.result[name]}>"
            component += "</li>"
        component += "</ul>"
    component += "</ul>"
    if report:
        component += (
            '<br> <input type="submit" value="Report Results"> '
            '<input name="update_results" type="hidden" value="true"></form>'
            "<form method='POST'> <input name='finish_round' type='submit' value='Finish Round'> </form>"
        )
    return component
