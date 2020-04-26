from django.urls import path
from pages.views import home, GamesList, privacy, delete_game

urlpatterns = [
    path(route='', view=home, name='home'),
    path(route='privacy/', view=privacy, name='privacy'),
    path('games/', GamesList.as_view(), name='games'),
    path('delete_game/<int:id>', view=delete_game, name='delete_game')
]