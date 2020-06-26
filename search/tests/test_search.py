import json
import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory



@pytest.mark.django_db
def test_search_murr_valid_params(create_murren, create_murr2):
    c = Client()
    search_path = reverse('search_murr')
    user_request = c.get(search_path, data={'search': '2'})
    assert user_request.status_code == 200
    assert b'1' in user_request.content


@pytest.mark.django_db
def test_search_murr_invalid_params(create_murren, create_murr2):
    c = Client()
    search_path = reverse('search_murr')
    user_request = c.get(search_path, data={'search': '3'}) # спотыкается здесь, ответ содержит пустую байт строку
    assert user_request.status_code == 200
    assert b'3' in user_request.content









