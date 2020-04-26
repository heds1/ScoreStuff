from django.urls import path
from pages.views import home, GamesList, privacy

urlpatterns = [
    path(route='', view=home, name='home'),
    path(route='privacy/', view=privacy, name='privacy'),
    path('games/', GamesList.as_view(), name='games'),
]