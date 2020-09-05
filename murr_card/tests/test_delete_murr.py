import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

Murren = get_user_model()


@pytest.mark.django_db
def test_delete_murr_card_success(create_murren, create_murr):
    murren = create_murren
    murr = create_murr
    client = APIClient()
    client.force_authenticate(user=murren)
    user_request = client.delete(f'/api/murr_card/{murr.id}/')
    assert user_request.status_code == 204


@pytest.mark.django_db
def test_delete_murr_card_error(create_murren, create_murr):
    murren = create_murren
    murr = create_murr
    client = APIClient()
    client.force_authenticate(user=murren)
    user_request = client.delete(f'/api/murr_card/{murr.pk}/')
    assert user_request.status_code == 204
