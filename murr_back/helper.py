import os

from django.contrib.auth import get_user_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAKE_MIGRATIONS = 'python manage.py makemigrations murr_card murren'
MAKE_MIGRATIONS_IN_DOCKER = 'docker-compose exec web python manage.py makemigrations murr_card murren'
DOCKER_COMPOSE_UP = 'docker-compose up -d --build'
MIGRATE = 'python manage.py migrate'


def create_superuser(name, email, password):
    user = get_user_model()
    user.objects.create_superuser(name, email, password)


def create_user(name, email, password):
    user = get_user_model()
    user.objects.create_user(name, email, password)
