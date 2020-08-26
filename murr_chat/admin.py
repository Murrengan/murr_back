from django.contrib import admin
from .models import MurrChat, MurrChatMessage, MurrChatMembers

admin.site.register(MurrChat)
admin.site.register(MurrChatMembers)
admin.site.register(MurrChatMessage)
