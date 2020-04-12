from django import forms
from .models import Game, Player, Round

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



