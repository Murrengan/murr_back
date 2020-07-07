from channels.routing import ProtocolTypeRouter, URLRouter

from murr_back.middleware import SocketTokenAuthMiddleware
from murr_chat.routing import websocket_urls

application = ProtocolTypeRouter({
    'websocket': SocketTokenAuthMiddleware(URLRouter(websocket_urls))
})
