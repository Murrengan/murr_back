from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

Murren = get_user_model()


class Command(BaseCommand):
    help = 'Подготовить свежий стенд / Prepare fresh stand'

    def handle(self, *args, **options):
        admin = Murren.objects.create_superuser('admin', 'admin@admin.com', 'admin')
        if admin:
            print("Администратор создан успешно")


