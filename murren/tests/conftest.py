import pytest
import yaml
from django.contrib.auth import get_user_model

Murren = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def yml_dataset():
    stream = open('dataset.yml', 'r')
    return yaml.safe_load(stream)


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def test_email():
    return 'testemail@testemail.testemail'


@pytest.fixture
def test_murren_name():
    return 'Greg'
