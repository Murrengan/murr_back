import json

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import modify_settings
from django.urls import reverse

Murren = get_user_model()


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

    url = yml_dataset['test_create_murren']['url_for_create_murren']
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert data['username'] in json.loads(response.content).values()
    assert data['email'] in json.loads(response.content).values()
    assert 'id' in json.loads(response.content).keys()
    assert len(Murren.objects.all()) == 1
    assert len(mail.outbox) == 1

    murren = Murren.objects.get(pk=1)
    assert murren.username == username
    assert murren.password is not None
    assert murren.is_active is False

    html_mail_body = mail.outbox[0].alternatives[0][0]
    assert username in html_mail_body

    raw_list = html_mail_body.split('___')
    uid, token = raw_list[1], raw_list[2]

    url = yml_dataset['test_create_murren']['url_for_activation_murren']
    data = {
        'uid': uid,
        'token': token,
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 204
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
