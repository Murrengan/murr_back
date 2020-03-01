from django.contrib.auth import get_user_model

#Local 
from server_settings.common import recaptcha_server_token, base_url
from murren.forms import MurrenSignupForm
from murren.models import EmailSalt


User = get_user_model()


def register(email, password, username):

    murren_data = {
        'username': username,
        'email': email,
        'password': password
    }

    form = MurrenSignupForm(murren_data)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(password)
        user.save()

        return {'error': False, 'user':user}
    else:
        return {'error': True, 'error_text': form.errors}

def reset_password(password, user):
    user.set_password(password)
    user.save()

    return True

def activate(user):
    user.is_active = True
    user.save()

    return True