import os

import pytest
import yaml
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

Murren = get_user_model()


@pytest.fixture
def api_client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def yml_dataset():
    dataset_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dataset.yml')
    stream = open(dataset_path, 'r')
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
