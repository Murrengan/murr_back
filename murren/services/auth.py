from django.contrib.auth import get_user_model

from murren.forms import MurrenSignupForm
from murren.models import EmailToken

import murren.services.email_confirm as confirm

User = get_user_model()


def register(data):

    form = MurrenSignupForm(data)
    
    if form.is_valid():
        user = form.save(commit=True)

        token = confirm.generate_email_token(user)

        url = confirm.generate_confirm_url('murren_email_activate', token)
        confirm.send_confirm('activation_email.html', '[murrengan] Активация аккаунта Муррена', \
                                                'Murrengan <murrengan.test@gmail.com>', user, url)

        return {'error': False, 'user': user}
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

    