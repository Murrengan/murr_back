import json
import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import modify_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

Murren = get_user_model()


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_create_murren(api_client, yml_dataset, test_password, test_email, test_murren_name):
    data = {
        'username': test_murren_name,
        'password': test_password,
        'email': test_email
    }

    url = reverse('murren_register')
    response = api_client.post(url, data, format='json')

    assert response.status_code == 200
    assert json.loads(response.content) == yml_dataset['test_create_murren']['response_on_sign_up']
    assert len(Murren.objects.all()) == 1
    assert len(mail.outbox) == 1
    murren = Murren.objects.get(pk=1)
    assert murren.is_active is False

    html_mail_body = mail.outbox[0].alternatives[0][0]
    assert test_murren_name in html_mail_body

    delimiters = ('activation_code=', '</span>')
    regex_pattern = '|'.join(map(re.escape, delimiters))
    splitted_html_mail = re.split(regex_pattern, html_mail_body)
    secret_code_index = splitted_html_mail.index(urlsafe_base64_encode(force_bytes(murren.email)))
    secret_code = splitted_html_mail[secret_code_index]
    assert secret_code in html_mail_body

    url = reverse('murren_activate')
    data = {
        'murren_email': secret_code
    }
    response = api_client.post(url, data, format='json')
    assert json.loads(response.content) == yml_dataset['test_create_murren']['response_on_activation']
    murren = Murren.objects.get(pk=1)
    assert murren.is_active is True

    data = {
        'username': test_murren_name,
        'password': test_password
    }
    url = reverse('obtain_token_pair')
    response = api_client.post(url, data, format='json')

    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

    url = reverse('get_tanochka_img')

    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == yml_dataset['test_create_murren']['auth_response']
