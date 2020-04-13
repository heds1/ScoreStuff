from django.db import models
from datetime import datetime
from django.utils.crypto import get_random_string

class Game(models.Model):
    """
    Game has a one-to-many relationship with Round (a Game may have several
    Rounds, but a Round may only belong to one Game).
    Game has a one-to-many relationship with Player (a Game may have several
    Players, but a Player may only belong to one Game. This may change in the
    future to a many-to-many relationship to allow tracking of player stats over
    several Games).
    """
    slug = models.SlugField(
        unique=True,
        blank=True) # only so I can migrate after initial migration....

    def save(self, *args, **kwargs):
        # if a slug doesn't exist (i.e., if this is the first time this has been
        # saved)
        if not self.slug:
            self.slug = get_random_string(7)
            # check for unique slug
            slug_is_wrong = True
            while slug_is_wrong:
                slug_is_wrong = False
                other_objs_with_slug = type(self).objects.filter(slug=self.slug)
                if len(other_objs_with_slug) > 0:
                    slug_is_wrong = True
                    self.slug = get_random_string(7)

        # save the object
        super().save(*args, **kwargs)
       

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('game', kwargs = {'slug': self.slug})


class Player(models.Model):
    """
    Player has a many-to-one relationship with Game (a Player can only belong to
    one Game, but a Game can have several Players).
    """
    name = models.CharField(
        max_length=30)
    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Round(models.Model):
    """
    Round has a many-to-one relationship with Game (a Round belongs to only one
    Game, but a Game may have several Rounds).
    """
    game = models.ForeignKey(
        to=Game,
        on_delete=models.CASCADE)
    


class Score(models.Model):
    """
    Score has a one-to-many relationship with Player (a Score can only belong to
    one Player, but a Player can have many Scores).
    Score has a one-to-many relationship with Round (a Score can only belong to
    one Round, but a Round can have many Scores).
    """
    # ensure only one score is added for a given Round/Player combination
    class Meta:
        unique_together = (("game_round", "player"), )
    
    game_round = models.ForeignKey(
        to=Round,
        on_delete=models.CASCADE)
    player = models.ForeignKey(
        to=Player,
        on_delete=models.CASCADE)
    value = models.IntegerField(
        default=0)

    def __str__(self):
        return "Round %s, Player = %s, Score = %s" % (self.game_round, self.player, self.value)
    

# python manage.py shell
# from scorer.models import Game,Player,Round,Score
# myg = Game.objects.get(slug='1XuB8Bk')
# myg.player_set.all()
# myp=myg.player_set.all()[1]

# newround = Round(game=myg)
# newscore = Score(game_round=newround, player=myg.player_set.all()[1], value=5)