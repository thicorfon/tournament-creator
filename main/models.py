from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    current_points = models.FloatField

    def __str__(self):
        return self.name


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
    desired_table_size = models.IntegerField
    status = models.CharField(
        max_length=60,
        choices=TournamentStatus.statuses,
        default=TournamentStatus.STARTED,
    )
