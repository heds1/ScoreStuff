from django.shortcuts import render
from django.urls import reverse
from scorer.forms import CreateGameForm
from scorer.models import Game, Round
from django.http import HttpResponseRedirect
from django.views.generic import ListView

def home(request):
    """
    Landing page. Request is dependent on user being logged in, and is based on
    'Create new game' button.
    """
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


class GamesList(ListView):
    """
    Return a list of all games for the logged-in user.
    """
    template_name = 'pages/games.html'
    context_object_name = 'games'
    model = Game

    # class Meta:
    #     ordering: 

    def get_queryset(self):
        """
        Return all games associated with User
        """
        queryset = super(GamesList, self).get_queryset()
        queryset = queryset.filter(organizer_id=self.request.user)
        return queryset


def privacy(request):
    return render(request, template_name='pages/privacy.html')