from django.db import models

# Create your models here.
from django.db import models

class GameSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    cash = models.IntegerField()

    financial = models.FloatField()
    human = models.FloatField()
    green = models.FloatField()
    resilience = models.FloatField()
    digital = models.FloatField()


class Decision(models.Model):
    game = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    choice = models.CharField(max_length=1)

    R = models.FloatField()
    E = models.FloatField()
    S = models.FloatField()
    B = models.FloatField()
    T = models.FloatField()
    P = models.FloatField()
    A = models.FloatField()