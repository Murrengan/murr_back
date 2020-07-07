from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from murr_chat.models import MurrChatMembers, MurrChat
from .base import BaseMurrChatConsumer

Murren = get_user_model()


class LobbyConsumer(BaseMurrChatConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.personal_murren_channel = None

    async def connect(self):
        await super().connect()
        self.personal_murren_channel = MurrChat.personal_murren_channel(self.scope['user'].id)
        await self.channel_layer.group_add(self.personal_murren_channel, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.personal_murren_channel, self.channel_name)
        await super().disconnect(code=code)

    async def gan__get_murren_chats_list(self, event):
        data = await self.get_murren_chats_list(self.scope['user'])
        await self._send_message(data, event=event['gan'])

    @database_sync_to_async
    def get_murren_chats_list(self, murren):
        chat_ids = list(MurrChatMembers.objects.filter(member=murren).values_list('chat_name', flat=True))
        result = []
        for i in MurrChat.objects.filter(id__in=chat_ids):
            result.append({'id': i.id, 'murr_chat_name': i.murr_chat_name, 'link': i.link})
        return result

    async def gan__get_murren_list(self, event):
        data = await self.get_murren_list(self.scope['user'])
        await self._send_message(data, event=event['gan'])

    @database_sync_to_async
    def get_murren_list(self, murren):
        murrens = Murren.objects.all().exclude(pk=murren.id)
        data = []
        for i in murrens:
            data.append({'id': i.id, 'murren_name': i.username})
        return data

    async def gan__create_murr_chat(self, event):
        murr_chat_name = event['data'].get('murr_chat_name')
        if not murr_chat_name:
            return await self._trow_error({'detail': 'Missing murr_chat_name'}, event=event['event'])
        data = await self.create_murr_chat(murr_chat_name, self.scope['user'])
        await self._send_message(data, event=event['gan'])

    @database_sync_to_async
    def create_murr_chat(self, murr_chat_name, murren):
        murr_chat = MurrChat(murr_chat_name=murr_chat_name)
        murr_chat.save()
        murr_chat_member = MurrChatMembers(member=murren, chat_name=murr_chat)
        murr_chat_member.save()
        return {'id': murr_chat.id, 'murr_chat_name': murr_chat.murr_chat_name, 'link': murr_chat.link}

    async def send_notice(self, event):
        await self._send_message(event['data']['data'], event=event['data']['gan'])
