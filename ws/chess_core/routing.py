from django.urls import re_path
from game.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r'play/$', GameConsumer.as_asgi()),
]