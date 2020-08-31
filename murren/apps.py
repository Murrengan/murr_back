from django.apps import AppConfig


class MurrenConfig(AppConfig):
    name = 'murren'

    # If we need to get photo from a social network. TBD
    # def ready(self):
    #     import murren.signals
