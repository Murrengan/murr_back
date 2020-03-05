from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from murren.models import Murren


class Command(BaseCommand):

    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(options['quantity']):
            try:
                user = Murren()
                user.email = fake.email()
                user.username = fake.name().replace(' ', '_')
                user.set_password('secret')
                user.is_active = True
                user.save()
            except IntegrityError:
                self.stdout.write(self.style.ERROR('This fake user is already '
                                                   'exists, skip this user.'))

        self.stdout.write(self.style.SUCCESS('Fake user created...'))

    def add_arguments(self, parser):
        parser.add_argument(
                '-q',
                type=int,
                dest='quantity',
                default=20
        )
