from django.shortcuts import render
from django.http import HttpResponseRedirect
from scorer.models import Game, Player, Score, Round
from .forms import AddPlayerForm, AddRoundForm, ScoreForm
from django.urls import reverse
from django.forms import modelformset_factory
from django.db.models import Sum

def game(request, slug):
    this_game = Game.objects.get(slug=slug)
    players = this_game.player_set.all()
    rounds = this_game.round_set.all()
    latest_round = rounds.last()
    add_player_form = AddPlayerForm(initial={'game': this_game})
    add_round_form = AddRoundForm(initial={'game': this_game})
    AddScoreFormSet = modelformset_factory(Score, form=ScoreForm, fields=('game_round','player','value'), extra=0)
    
    # get total scores
    # https://stackoverflow.com/questions/45547674/how-to-execute-a-group-by-count-or-sum-in-django-orm/45547675
    running_scores = Score.objects.filter(game_round__id__in=rounds, player_id__in=players).values('player_id').order_by('player_id').annotate(total=Sum('value'))
        
    # the queryset filtering won't work if we haven't added a Round to this game
    # yet, so check if that's the case; otherwise, create empty formset
    if latest_round is not None and players is not None:
        formset = AddScoreFormSet(queryset=Score.objects.filter(player_id__in=players, game_round__id__startswith=latest_round.id))
    else:
        formset = AddScoreFormSet(queryset=Score.objects.none())

    # if POST (someone's clicked a button...)
    if request.method == 'POST':
       
        # if the POST request is to add another Player
        if 'add_player' in request.POST:
            add_player_form = AddPlayerForm(request.POST)
            if add_player_form.is_valid():
                add_player_form.save()
                # get this new player and add a placeholder score of 0
                new_player = this_game.player_set.all().last()
                new_score = Score(game_round=latest_round, player=new_player, value=0)
                new_score.save()

                return HttpResponseRedirect(reverse('game', kwargs = {'slug': this_game.slug}))
                
        # if the POST request is to add another set of Scores
        # ... also add another empty Round
        elif 'add_score' in request.POST:
            formset = AddScoreFormSet(request.POST)
            # if formset.is_valid():
            formset.save()

            new_round = Round(game=this_game)
            new_round.save()   
            new_round = this_game.round_set.all().last()
            for player in players:
                new_score = Score(game_round=new_round, player=player, value=0)
                new_score.save()         

            return HttpResponseRedirect(reverse('game', kwargs = {'slug': this_game.slug}))


    # else this is a GET request, just render blank forms
    else:
        # only add player to the current game by default. selector is hidden.
        add_player_form = AddPlayerForm(initial={'game': this_game})
        add_round_form = AddRoundForm(initial={'game': this_game})

    context = {
        "this_game": this_game,
        "add_player_form": add_player_form,
        "add_round_form": add_round_form,
        "players": players,
        "running_scores": running_scores,
        "rounds": rounds,
        "latest_round": latest_round,
        "formset": formset,
    }

    return render(request, template_name='scorer/game.html', context=context)


