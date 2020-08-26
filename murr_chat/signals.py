from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save

from .models import MurrChatMessage, MurrChatMembers, MurrChat


def send_murr_chat_message(data, murr_chat_name):
    async_to_sync(get_channel_layer().group_send)(murr_chat_name, data)


def new_murr_chat_member(sender, instance, created, **kwargs):
    if created:
        first_murr_chat_member = MurrChatMembers.objects.filter(chat_name=instance.chat_name).order_by('id').first()
        if first_murr_chat_member.member.id != instance.member.id:
            data = {
                'type': 'send_notice',
                'data': {
                    'gan': 'new_murr_chat_member',
                    'data': {
                        'id': instance.chat_name.id,
                        'name': instance.chat_name.murr_chat_name,
                        'link': instance.chat_name.link
                    }
                }
            }
            murr_chat_name = MurrChat.personal_murren_channel(instance.member.id)
            send_murr_chat_message(data, murr_chat_name)


def new_murr_chat_message(sender, instance, created, **kwargs):
    if created:
        data = {
            'type': 'send_notice',
            'data': {
                'gan': 'new_murr_chat_message',
                'data': {
                    'id': instance.id,
                    'murr_chat_id': instance.chat_name.id,
                    'message': instance.message
                }
            }
        }
        murr_chat_members = MurrChatMembers.objects.filter(chat_name=instance.chat_name).exclude(member=instance.member)
        for murren in murr_chat_members:
            murr_chat_name = MurrChat.personal_murren_channel(murren.member.id)
            send_murr_chat_message(data, murr_chat_name)


post_save.connect(new_murr_chat_member, sender=MurrChatMembers, dispatch_uid='new_murr_chat_member')
post_save.connect(new_murr_chat_message, sender=MurrChatMessage, dispatch_uid='new_murr_chat_message')
