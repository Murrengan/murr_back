import json
import re
import pytest

from django.core import mail
from django.test import modify_settings
from django.urls import reverse


def _token_find_in_mail():
    html_mail_body = mail.outbox[0].alternatives[0][0]
    matched = re.findall(r'\w{64}', html_mail_body)
    return matched[0]


def _create_new_murren(model, username, email, password):
    return model.objects.create_user(username=username, email=email, password=password)


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_empty_body(api_client, yml_dataset):
    response = api_client.post(reverse('confirm_new_password'), None, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['empty_body']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_not_token(api_client, yml_dataset):
    response = api_client.post(reverse('confirm_new_password'), {}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['not_token']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_token_is_empty(api_client, yml_dataset):
    response = api_client.post(reverse('confirm_new_password'), {'token': ''}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['token_is_empty']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_password_is_empty(api_client, yml_dataset):
    response = api_client.post(reverse('confirm_new_password'),
                               {'token': 'token', 'password': ''}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['password_is_empty']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_token_is_error(api_client, test_password, yml_dataset):
    response = api_client.post(reverse('confirm_new_password'),
                               {'token': 'token', 'password': test_password}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['token_is_error']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_password_match(api_client, test_murren_name, django_user_model, test_email,
                        test_password, yml_dataset):
    _create_new_murren(model=django_user_model, username=test_murren_name, email=test_email,
                       password=test_password)
    
    api_client.post(reverse('reset_password'), {'email': test_email}, format='json')
    
    token = _token_find_in_mail()
    assert token
    
    response = api_client.post(reverse('confirm_new_password'),
                               {'token': token, 'password': test_password},
                               format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['password_match']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_password_is_already_changed(api_client, test_murren_name, django_user_model,
                                     test_email, test_password, yml_dataset):
    _create_new_murren(model=django_user_model, username=test_murren_name, email=test_email,
                       password=test_password)
    
    api_client.post(reverse('reset_password'), {'email': test_email}, format='json')
    
    token = _token_find_in_mail()
    assert token
    
    response1 = api_client.post(reverse('confirm_new_password'),
                                {'token': token, 'password': f'{test_password}-1'},
                                format='json')
    assert json.loads(response1.content) == yml_dataset[
        'test_confirm_new_password']['new_password_successful']
    
    response2 = api_client.post(reverse('confirm_new_password'),
                                {'token': token, 'password': f'{test_password}-2'},
                                format='json')
    
    assert json.loads(response2.content) == yml_dataset[
        'test_confirm_new_password']['password_is_already_changed']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_new_password_successful(api_client, test_murren_name, django_user_model, test_email,
                                 test_password, yml_dataset):
    _create_new_murren(model=django_user_model, username=test_murren_name, email=test_email,
                       password=test_password)
    
    api_client.post(reverse('reset_password'), {'email': test_email}, format='json')
    
    token = _token_find_in_mail()
    assert token
    
    response = api_client.post(reverse('confirm_new_password'),
                               {'token': token, 'password': f'{test_password}-1'},
                               format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_confirm_new_password']['new_password_successful']
