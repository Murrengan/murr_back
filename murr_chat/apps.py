from django.apps import AppConfig


class MurrChatConfig(AppConfig):
    name = 'murr_chat'

    def ready(self):
        import murr_chat.signals  # noqa
