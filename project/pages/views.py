from django.shortcuts import render
from django.urls import reverse
from scorer.forms import CreateGameForm
from scorer.models import Game, Round
from django.http import HttpResponseRedirect

def home(request):

    # if the 'GET STARTED' button is clicked, we need to process the form data
    # (which basically just creates a game)
    if request.method == 'POST':
        form = CreateGameForm(request.POST)
        if form.is_valid():
            new_game = Game()
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