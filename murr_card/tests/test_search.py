import json
import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APIClient


@pytest.mark.django_db
def test_search_murr_valid_params(create_murren, create_murr1):
    c = APIClient()
    search_path = reverse('search_murr')
    user_request = c.get(search_path, data={'search': '1'})
    responsing = json.dumps(user_request.data['results'])
    assert user_request.status_code == 200
    assert 'danl' in responsing


@pytest.mark.django_db
def test_search_murr_invalid_params(create_murren, create_murr1):
    c = APIClient()
    search_path = reverse('search_murr')
    user_request = c.get(search_path, data={'search': '3'})
    responsing = json.dumps(user_request.data['results'])
    assert user_request.status_code == 200
    assert 'danl' not in responsing







