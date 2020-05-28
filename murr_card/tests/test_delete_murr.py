import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

Murren = get_user_model()


@pytest.mark.django_db
def test_delete_murr_valid_params(create_murren, create_murr):
    user1 = create_murren
    murr1 = create_murr.title
    client = APIClient()
    client.force_authenticate(user=user1)
    delete_path = reverse('MurrCardView')
    user_request = client.delete(delete_path, data={'murr_id': murr1, 'owner_id': 1}, format='json')
    assert user_request.status_code == 204

@pytest.mark.django_db
def test_delete_murr_invalid_params(create_murren, create_murr):
    user1 = create_murren
    murr1 = create_murr.title
    client = APIClient()
    client.force_authenticate(user=user1)
    delete_path = reverse('MurrCardView')
    user_request = client.delete(delete_path, data={'murr_id': murr1, 'owner_id': 2}, format='json')
    assert user_request.status_code == 400
