from django.urls import path

from murr_chat.consumers.lobby import LobbyConsumer
from murr_chat.consumers.murr_chat import MurrChatConsumer

websocket_urls = [
    path('ws/murr_chat/lobby/', LobbyConsumer),
    path('ws/murr_chat/<int:chat_id>/', MurrChatConsumer),
]
