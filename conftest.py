import pytest
from django.contrib.auth import get_user_model

from murr_card.models import MurrCard

Murren = get_user_model()


@pytest.fixture
def create_murren():
    murren = Murren.objects.create_user(username='TestMurrenName',
                                        password='SecretPassword',
                                        email='test_email@mail.ru')
    murren.save()
    return murren


@pytest.fixture
def create_murr():
    murren = Murren.objects.get(pk=1)
    murr = MurrCard.objects.create(
        title="It's my cool sexy title",
        content="Halo, dat's not me",
        owner=murren,
    )
    return murr
