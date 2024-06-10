from django.db import models


class PlayerStatus:
    DROPPED = "d"
    ACTIVE = "a"

    statuses = ((DROPPED, "dropped"), (ACTIVE, "active"))


class Player(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    current_points = models.FloatField(default=0)
    current_status = models.CharField(
        max_length=60, default=PlayerStatus.ACTIVE, choices=PlayerStatus.statuses
    )

    def __str__(self):
        return self.name

    @classmethod
    def create_new_player(cls, name):
        player = cls(name=name)
        return player


################################
class TournamentStatus:
    STARTED = "s"
    WAITING_ROUND = "wr"
    ACTIVE_ROUND = "ar"
    FINISHED = "f"

    statuses = (
        (STARTED, "started"),
        (WAITING_ROUND, "waiting_round"),
        (ACTIVE_ROUND, "active_round"),
        (FINISHED, "finished"),
    )


class Tournament(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    players = models.ManyToManyField(Player)
    desired_table_size = models.IntegerField(default=4)
    current_round = models.IntegerField(default=0)
    status = models.CharField(
        max_length=60,
        choices=TournamentStatus.statuses,
        default=TournamentStatus.STARTED,
    )

    @classmethod
    def create_new_tournament(cls, name):
        tournament = cls(name=name)
        return tournament


##################################


class RoundStatus:
    STARTED = "s"
    FINISHED = "f"

    statuses = ((STARTED, "started"), (FINISHED, "finished"))


class Round(models.Model):
    number = models.IntegerField()
    players = models.ManyToManyField(Player)
    status = models.CharField(
        max_length=60, choices=RoundStatus.statuses, default=RoundStatus.STARTED
    )
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    @classmethod
    def create_new_round(cls, number, players, tournament):
        round = cls()
        round.number = number
        round.tournament = tournament
        round.save()
        for player in players:
            round.players.add(player)
        round.save()
        return round


class MatchStatus:
    STARTED = "s"
    FINISHED = "f"

    statuses = ((STARTED, "started"), (FINISHED, "finished"))


class Match(models.Model):
    players = models.ManyToManyField(Player)
    result = models.JSONField(default=dict, null=True)
    status = models.CharField(
        max_length=60, choices=MatchStatus.statuses, default=MatchStatus.STARTED
    )
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    number = models.IntegerField()

    @classmethod
    def create_new_match(cls, players, round, number):
        match = cls()
        match.round = round
        match.number = number
        match.save()
        results = {}
        for player in players:
            match.players.add(player)
            results[player.name] = -1
        match.result = results
        match.save()
        return match

    def report_result(self, match_result):
        for placing in match_result:
            name = placing[0]
            points = placing[1]
            self.result[name] = points
        self.status = MatchStatus.FINISHED
        self.save()
        return self
