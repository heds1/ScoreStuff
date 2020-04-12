from django.urls import path
from .views import game

urlpatterns = [
    path(route='<slug:slug>/', view=game, name='game'),
]