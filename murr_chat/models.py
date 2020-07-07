from django.contrib.auth import get_user_model
from django.db import models

Murren = get_user_model()


class MurrChat(models.Model):
    murr_chat_name = models.CharField(max_length=244)

    def __str__(self):
        return self.murr_chat_name

    @classmethod
    def chat_name(cls, group_id):
        return f'{group_id}'

    @classmethod
    def personal_murren_channel(cls, murren_id):
        return f'{murren_id}'

    @property
    def link(self):
        return f'/ws/murr_chat/{self.id}/'


class MurrChatMembers(models.Model):
    member = models.ForeignKey(Murren, related_name='murr_chat_member', on_delete=models.CASCADE, null=True)
    chat_name = models.ForeignKey(MurrChat, related_name='murr_chat_member', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.member.username


class MurrChatMessage(models.Model):
    member = models.ForeignKey(Murren, related_name='murren_message', on_delete=models.CASCADE, null=True)
    chat_name = models.ForeignKey(MurrChat, related_name='murr_chat_message', on_delete=models.CASCADE, null=True)
    message = models.TextField(default='')

    def __str__(self):
        return self.message
