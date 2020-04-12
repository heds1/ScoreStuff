from django.shortcuts import render
from django.http import HttpResponseRedirect
from scorer.models import Game, Player
from .forms import AddPlayerForm, AddRoundForm
from django.urls import reverse

def game(request, slug):
    this_game = Game.objects.get(slug=slug)
    players = this_game.player_set.all()

    # if POST (someone's clicked a button...)
    if request.method == 'POST':
        
        # if the POST request is to add another Round
        if 'add_round' in request.POST:
            add_round_form = AddRoundForm(request.POST)
            # add_player_form = AddPlayerForm(initial={'game': this_game})
            if add_round_form.is_valid():
                new_round = add_round_form.save()
                return HttpResponseRedirect(reverse('game', kwargs = {'slug': this_game.slug}))
        
        # if the POST request is to add another Player
        elif 'add_player' in request.POST:
            add_player_form = AddPlayerForm(request.POST)
            if add_player_form.is_valid():
                new_player = add_player_form.save()
                return HttpResponseRedirect(reverse('game', kwargs = {'slug': this_game.slug}))

    # else this is a GET request, just render blank forms
    else:
        add_player_form = AddPlayerForm(
            # only add player to the current game by default. selector is hidden.
            initial={'game': this_game})

        add_round_form = AddRoundForm(initial={'game': this_game})

    context = {
        "this_game": this_game,
        "add_player_form": add_player_form,
        "add_round_form": add_round_form,
        "players": players,
    }


    return render(request, template_name='scorer/game.html', context=context)


