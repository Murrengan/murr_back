import pytest
from django.contrib.auth import get_user_model

from murr_card.models import MurrCard

Murren = get_user_model()


@pytest.fixture
def create_murren():
    user1 = Murren.objects.create_user(username='danl',
                                       password='123k45',
                                       email='integritys@mail.com')
    user1.save()
    return user1


@pytest.fixture
def create_murr():
    user1 = Murren.objects.get(pk=1)
    one_murr = MurrCard.objects.create(
        title=1,
        content="Halo, dat's not me",
        owner=user1,
    )
    return one_murr
