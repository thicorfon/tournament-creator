# Generated by Django 4.2.13 on 2024-05-28 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_player_current_points_tournament"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="current_status",
            field=models.CharField(
                choices=[("d", "dropped"), ("a", "active")], default="a", max_length=60
            ),
        ),
    ]
