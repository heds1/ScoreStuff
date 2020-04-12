from django.urls import path
from .views import home, privacy

urlpatterns = [
    path(route='', view=home, name='home'),
    path(route='privacy/', view=privacy, name='privacy')
]