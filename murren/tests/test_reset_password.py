import json
import re
import pytest

from django.core import mail
from django.test import modify_settings
from django.urls import reverse

from murren.models import PasswordReset


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_empty_body(api_client, yml_dataset):
    response = api_client.post(reverse('reset_password'), None, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['empty_body']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_not_filed_email(api_client, yml_dataset):
    response = api_client.post(reverse('reset_password'), {}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['not_filed_email']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_reset_password_empty_email(api_client, yml_dataset):
    response = api_client.post(reverse('reset_password'), {'email': ''}, format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['empty_email']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_not_fround_email(api_client, test_email, yml_dataset):
    response = api_client.post(reverse('reset_password'), {'email': test_email},
                               format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['not_fround_email']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_not_active_murren(api_client, test_email, test_password,
                           test_murren_name, django_user_model, yml_dataset):
    murren = django_user_model(username=test_murren_name, email=test_email)
    murren.is_active = False
    murren.set_password(test_password)
    murren.save()
    
    response = api_client.post(reverse('reset_password'), {'email': test_email},
                               format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['not_active_murren']


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_create_token_reset_password(api_client, test_email, test_password,
                                     test_murren_name, django_user_model):
    django_user_model.objects.create_user(test_murren_name, email=test_email,
                                          password=test_password)
    
    api_client.post(reverse('reset_password'), {'email': test_email}, format='json')
    
    assert len(mail.outbox) == 1
    html_mail_body = mail.outbox[0].alternatives[0][0]
    assert test_murren_name in html_mail_body
    matched = re.findall(r'\w{64}', html_mail_body)
    assert matched[0]
    
    password = PasswordReset.objects.get(token=matched[0])
    
    assert password.token == matched[0]


@pytest.mark.django_db
@modify_settings(MIDDLEWARE={'remove': 'murr_back.middleware.CheckRecaptchaMiddleware'})
def test_send_email(api_client, test_email, test_password,
                    test_murren_name, django_user_model, yml_dataset):
    django_user_model.objects.create_user(test_murren_name, email=test_email,
                                          password=test_password)
    
    response = api_client.post(reverse('reset_password'), {'email': test_email},
                               format='json')
    
    assert json.loads(response.content) == yml_dataset[
        'test_reset_password']['send_email']
