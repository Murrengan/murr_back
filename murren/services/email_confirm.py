from django.contrib.auth import get_user_model
from django.utils.dateformat import format
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail

import hashlib
import random
import string
import time
from datetime import datetime, timedelta

#Local 
from server_settings.common import recaptcha_server_token, base_url
from murren.forms import MurrenSignupForm
from murren.models import EmailSalt

User = get_user_model()

def generate_email_token(user):
    letters = string.ascii_lowercase
    salt_str =  ''.join(random.choice(letters) for i in range(8))

    salt = EmailSalt.objects.create(salt=salt_str, murren=user, time=datetime.now())

    token = urlsafe_base64_encode(force_bytes(str(salt.pk) + '$' + hashlib.sha1(str(user.email).encode('utf-8') + str(user.pk).encode('utf-8') + str(salt_str).encode('utf-8')).hexdigest()))    
    return token

def check_email_token(token, interval, count):
    token = force_text(urlsafe_base64_decode(token))
    token = token.split('$')

    try:
        salt = EmailSalt.objects.get(pk=int(token[0]))
        user = User.objects.get(pk=salt.murren.pk)

        hash = hashlib.sha1(str(user.email).encode('utf-8') + str(user.pk).encode('utf-8') + str(salt.salt).encode('utf-8')).hexdigest()


        if hash == token[1] and int(format(salt.time, 'U')) > int(time.time()) - interval * 60 * 60 and check_user_tokens(user, interval, count) and not salt.is_used:
            salt.is_used = True
            salt.save()
            return {'error': False, 'user':user}
        else:
            return {'error': True, 'error_text': 'token_error'}
    except(TypeError, ValueError, OverflowError, EmailSalt.DoesNotExist, User.DoesNotExist) as error:
        return {'error': True,  'error_text': error.args[0]}

def check_user_tokens(user, interval, count):
    salts = EmailSalt.objects.filter(murren=user, time__gte=datetime.now() - timedelta(hours=24)).count()
    if salts <= count:
        return True
    else:
        return False

def send_confirm(template, subject, email_to, email_from, token, user, url): 
    message = base_url + '/'+ url +'/?activation_code=' + token

    html_data = render_to_string('reset_email.html', {'uri': message, 'murren_name': user.username})
    send_mail(subject, None, email_from, [email_to], html_message=html_data)

    return True