from django.shortcuts import render
from django.urls import reverse
from scorer.forms import CreateGameForm
from scorer.models import Game, Round
from django.http import HttpResponseRedirect

def home(request):

    # create new room
    if request.method == 'POST':

        # instantiate form
        form = CreateGameForm(request.POST)

        if form.is_valid():

            # set the organizer to the current user
            new_game = form.save(commit=False)
            new_game.organizer = request.user
            new_game.save()

            # initialise game with first Round
            new_round = Round(game=new_game)
            new_round.save()

            # redirect to new game room
            return HttpResponseRedirect(reverse('game', kwargs = {'slug': new_game.slug}))
    
    # else request is GET, just render form
    else:
        form = CreateGameForm()

    return render(request, 'pages/home.html', {'form': form})


def privacy(request):
    return render(request, template_name='pages/privacy.html')