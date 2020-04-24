from django.urls import path

from murr_chat.consumers.lobby import LobbyConsumer

websocket_urls = [
    path('ws/murr_chat/lobby/', LobbyConsumer),
]
