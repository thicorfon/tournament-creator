from django.contrib import admin

from .models import Tournament, Player, Round, Match

admin.site.register(Tournament)
admin.site.register(Player)
admin.site.register(Round)
admin.site.register(Match)
