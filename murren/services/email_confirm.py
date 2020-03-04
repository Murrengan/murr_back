from django.contrib.auth import get_user_model
from django.utils.dateformat import format
from django.http import JsonResponse
from django.utils.encoding import force_bytes, \
    force_text
from django.utils.http import urlsafe_base64_encode, \
    urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail

import hashlib
import random
import string
import time
import hmac
from uuid import uuid4
import crypt
from datetime import datetime, timedelta

from common_helpers.global_variables import base_url
from murren.forms import MurrenSignupForm
from murren.models import EmailToken

User = get_user_model()

def generate_email_token(user):
    key = str(uuid4())
    salt = crypt.mksalt(crypt.METHOD_SHA512)
    token = hmac.new(key.encode(), salt.encode(), hashlib.sha256).hexdigest()

    EmailToken.objects.create(token=token, murren=user)   
    return token

def check_email_token(token, lifetime):
    token = force_text(urlsafe_base64_decode(token))

    try:
        token = EmailToken.objects.get(token=token)
        user = token.murren
    except EmailToken.DoesNotExist as error:
        return {'error': True,  'type': 'email_token'}

    if int(format(token.time, 'U')) < int(format(datetime.now() - lifetime, 'U')):
        return {'error': True,  'type': 'email_token'}

    token.delete()

    return {'error': False, 'user': user}

def generate_confirm_url(type, token):
    token = urlsafe_base64_encode(force_bytes(token))

    return base_url + '/'+ type +'/?activation_code=' + token

def send_confirm(template, subject, email_from, user, url):
    html_data = render_to_string(template, {'uri': url, 'murren_name': user.username})
    send_mail(subject, None, email_from, [user.email], html_message=html_data)

    return {'error': False}