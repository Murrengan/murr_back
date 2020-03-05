import json
import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import modify_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from murren.forms import MurrenSignupForm

Murren = get_user_model()

def _token_in_mail(type):
    html_mail = mail.outbox[0].alternatives[0][0]
    token_re = re.findall(f'{type}/([A-Za-z0-9]+(?:[\s-][A-Za-z0-9]+)*)', html_mail)
    token = token_re[0]
    return token

@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_create_murren(api_client, yml_dataset, test_password, test_email, test_murren_name):
    password = test_password
    email = test_email
    username = test_murren_name
    data = {
        'username': username,
        'password': password,
        'email': email,
    }

    url = reverse('murren_register')
    response = api_client.post(url, data, format='json')

    assert response.status_code == 200
    assert json.loads(response.content) == yml_dataset['test_create_murren']['response_on_sign_up']
    assert len(Murren.objects.all()) == 1
    assert len(mail.outbox) == 1
    murren = Murren.objects.get(pk=1)
    assert murren.username == username
    assert murren.password is not None
    assert murren.is_active is False

    html_mail_body = mail.outbox[0].alternatives[0][0]
    assert username in html_mail_body

    activation_code = _token_in_mail('murren_email_activate')
    
    url = reverse('murren_activate')
    data = {
        'email_token': activation_code,
    }
    response = api_client.post(url, data, format='json')
    assert json.loads(response.content) == yml_dataset['test_create_murren']['response_on_activation']
    murren = Murren.objects.get(pk=1)
    assert murren.is_active is True

    data = {
        'username': username,
        'password': password,
    }
    url = reverse('obtain_token_pair')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200, json.loads(response.content)

    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    url = reverse('get_tanochka_img')

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == yml_dataset['test_create_murren']['auth_response']


@pytest.mark.django_db
def test_short_password(yml_dataset, test_murren_name, test_email):
    data = {
        'username': test_murren_name,
        'email': test_email,
        'password': yml_dataset['test_short_password']['week_password']
    }
    form = MurrenSignupForm(data)
    assert form.is_valid() is False
    assert yml_dataset['test_short_password']['error_text'] in form.errors.get('password')


@pytest.mark.django_db
def test_common_password(yml_dataset, test_murren_name, test_email):
    data = {
        'username': test_murren_name,
        'email': test_email,
        'password': yml_dataset['test_common_password']['week_password']
    }
    form = MurrenSignupForm(data)
    assert form.is_valid() is False
    assert yml_dataset['test_common_password']['error_text'] in form.errors.get('password')


@pytest.mark.django_db
def test_numeric_password(yml_dataset, test_murren_name, test_email):
    data = {
        'username': test_murren_name,
        'email': test_email,
        'password': yml_dataset['test_numeric_password']['week_password']
    }
    form = MurrenSignupForm(data)
    assert form.is_valid() is False
    assert yml_dataset['test_numeric_password']['error_text'] in form.errors.get('password')
