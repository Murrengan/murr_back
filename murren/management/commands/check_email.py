from django.core.management.base import BaseCommand
from murren.models import Murren
from datetime import datetime, timezone, timedelta


class Command(BaseCommand):
    help = 'Checking email field'

    def handle(self, *args, **options):
        users = Murren.objects.all()
        now = datetime.now(timezone.utc)

        for user in users:
            if user.is_active != True:
                if now - user.date_joined > timedelta(2):
                    user.delete()
            if user.is_active == True:
                    user.email_check = 1

