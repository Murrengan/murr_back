from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from murr_chat.models import MurrChatMembers, MurrChat

from .base import BaseMurrChatConsumer

Murren = get_user_model()


class LobbyConsumer(BaseMurrChatConsumer):

    async def gan__get_murr_chat_list_with_murren(self, event):
        """
        Выводит список всех чатов, в которых состоит Муррен
        Displays a list of all the chats that Murren is a member of
        """
        data = await self.get_murr_chat_list_with_murren(self.scope['user'])
        await self._send_message(data, event=event['gan'])

    @database_sync_to_async
    def get_murr_chat_list_with_murren(self, murren):
        chat_ids = list(MurrChatMembers.objects.filter(member=murren).values_list('chat_name', flat=True))
        result = []
        for i in MurrChat.objects.filter(id_in=chat_ids):
            result.append({'id': i.id, 'murr_chat_name': i.murr_chat_name, 'link': i.link})
        return result

    async def gan__get_murren_list(self, event):
        data = self.get_murren_list(self.scope['user'])
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
