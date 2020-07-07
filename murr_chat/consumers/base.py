from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model

Murren = get_user_model()


class BaseMurrChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.scope["user"] = await self.get_user(self.scope["user"])
        await self.accept()
        if 'user' not in self.scope or self.scope['user'].is_anonymous:
            await self._send_message({'detail': 'Authorization failed'})
            await self.close(code=1000)
            return

    @database_sync_to_async
    def get_user(self, pk):
        murren = Murren.objects.get(id=pk)
        return murren

    async def receive_json(self, content, **kwargs):
        message = await self.parse_content(content)
        if message:
            event = message['gan']
            method = getattr(self, f'gan__{event}', self.method_undefined)
            await method(message)
        else:
            await self._trow_error({'detail': 'Invalid message'})

    @classmethod
    async def parse_content(cls, content):
        if isinstance(content, dict) and isinstance(content.get('gan'), str) and isinstance(content.get('data'),
                                                                                            dict):
            return content

    async def _group_send(self, data, event=None):
        data = {'type': 'proxy.group.send', 'data': data, 'gan': event}
        await self.channel_layer.group_send(self.chat_name, data)

    async def proxy_group_send(self, event):
        await self._send_message(event['data'], event=event.get('gan'))

    async def method_undefined(self, message):
        await self._trow_error({'detail': 'Unknown event'}, event=message['event'])

    async def _send_message(self, data, event=None):
        await self.send_json(content={'status': 'ok', 'data': data, 'gan': event})

    async def _trow_error(self, data, event=None):
        await self.send_json(content={'status': 'error', 'data': data, 'gan': event})
