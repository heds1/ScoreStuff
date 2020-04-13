from django import forms
from .models import Game, Player, Round, Score
from django.forms import modelformset_factory


class CreateGameForm(forms.Form):
    pass


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'game']


class AddRoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['game']


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['game_round', 'player', 'value']
