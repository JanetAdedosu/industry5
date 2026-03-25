from django.urls import path
from .views import game_view, process_decision

urlpatterns = [
    path('', game_view, name='game'),
    path('process/', process_decision),
]