import pytest
from django.contrib.auth import get_user_model

from murr_card.models import MurrCard

Murren = get_user_model()


@pytest.fixture
def create_murren():
    murren = Murren.objects.create_user(
        username='TestMurrenName',
        password='SecretPassword',
        email='test_email@mail.ru',
        is_banned=False,
    )
    murren.save()
    return murren


@pytest.fixture
def create_murr():
    murren = Murren.objects.get(pk=1)
    murr = MurrCard.objects.create(
        title=1,
        content="Halo, dat's not me",
        owner=murren,
    )
    return murr


@pytest.fixture
def create_murren_is_banned():
    murren = Murren.objects.create_user(
        username='TestMurrenName',
        password='SecretPassword',
        email='test_email@mail.ru',
        is_banned=True,
    )
    murren.save()
    return murren
