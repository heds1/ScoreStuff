from django.forms import ModelForm
from .models import Game, Player, Round, Score
from django.forms import modelformset_factory


class CreateGameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ['organizer']


class AddPlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'game']


class AddRoundForm(ModelForm):
    class Meta:
        model = Round
        fields = ['game']


class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ['game_round', 'player', 'value']
