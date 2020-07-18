from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from murr_chat.models import MurrChatMembers, MurrChat, MurrChatMessage
from .base import BaseMurrChatConsumer


class MurrChatConsumer(BaseMurrChatConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = None
        self.murr_chat_members = []
        self.chat_name = f'{self.chat_id}'

    async def connect(self):
        await super().connect()
        chat = await self.get_chat()
        if not chat:
            await self._trow_error({'detail': 'Murr chat not found'})
            await self.close()
            return
        murr_chat_members = await self.get_murr_chat_members()
        if self.scope['user'].id not in murr_chat_members:
            await self._trow_error({'detail': 'Murren id not in murr_chat_members'})
            await self.close()
            return
        await self.channel_layer.group_add(self.chat_name, self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)
        await super().disconnect(code=code)

    async def gan__add_murr_chat_member(self, event):
        murren_id = event['data'].get('murren_id')
        if not murren_id:
            return await self._trow_error({'detail': 'Missing murren_id'}, event=event['event'])
        await self.add_murr_chat_member(murren_id)
        murr_chat_members = await self.get_murr_chat_members()
        return await self._send_message(murr_chat_members, event=event['gan'])

    @database_sync_to_async
    def add_murr_chat_member(self, murren_id):
        murren = get_user_model().objects.filter(pk=murren_id).first()
        if murren:
            murr_chat_member, _ = MurrChatMembers.objects.get_or_create(chat_name=self.chat, member=murren)

    async def gan__send_message(self, event):
        message = event['data'].get('message')
        if not message:
            return await self._trow_error({'detail': 'Missing message'}, event=event['gan'])
        await self.save_message(message, self.scope['user'])
        data = {
            'murren_name': self.scope['user'].username,
            'message': event['data']['message']
        }
        return await self._group_send(data, event=event['gan'])

    async def gan__list_messages(self, event):
        messages = await self.get_messages()
        return await self._send_message(messages, event=event['gan'])

    @database_sync_to_async
    def get_chat(self):
        chat = MurrChat.objects.filter(pk=self.chat_id).first()
        if chat:
            self.chat = chat
        return chat

    @database_sync_to_async
    def get_murr_chat_members(self):
        murr_chat_members = list(MurrChatMembers.objects.filter(chat_name=self.chat).values_list('member', flat=True))
        self.murr_chat_members = murr_chat_members
        return murr_chat_members

    @database_sync_to_async
    def save_message(self, message, murren):
        m = MurrChatMessage(member=murren, chat_name=self.chat, message=message)
        m.save()

    @database_sync_to_async
    def get_messages(self):
        messages = MurrChatMessage.objects.select_related('member').filter(chat_name=self.chat_name).order_by('id')
        data = []
        for message in messages:
            data.append({'id': message.id, 'username': message.member.username, 'message': message.message})
        return data
