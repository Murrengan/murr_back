from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.encoding import force_bytes, \
    force_text
from django.utils.http import urlsafe_base64_encode, \
    urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
import json

# 3rd party
from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# local
from murren.serializers import MurrenSerializers, \
    PublicMurrenInfoSerializers
from server_settings.common import base_url
from .forms import MurrenSignupForm
from .models import PasswordReset
from .utils import create_token_reset_password

Murren = get_user_model()


class MurrensMethods(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        r = Murren.objects.get(id=request.user.id)
        data = {'murren_name': r.username}
        return Response(data)


class GetTanochkaImg(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {'img_url': '/media/tanochka.jpg'}
        return Response(data)


class PublicMurrenInfo(APIView):

    def get(self, request, pk):
        r = Murren.objects.get(id=pk)
        serializer = PublicMurrenInfoSerializers(r, context={'request': request})
        return Response(serializer.data)


class GetAllMurrens(APIView):

    def get(self, request):
        qs = Murren.objects.filter(is_active=True)
        serializer = MurrenSerializers(qs, many=True)
        return Response(serializer.data)


def murren_register(request):
    if request.method == 'POST':

        json_data = json.loads(request.body)

        murren_data = {
            'username': json_data['username'],
            'email': json_data['email'],
            'password': json_data['password'],
        }

        form = MurrenSignupForm(murren_data)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.set_password(murren_data.get('password'))
            user.save()

            message = base_url + '/murren_email_activate/?activation_code=' \
                      + urlsafe_base64_encode(force_bytes(user.email))
            subject = '[murrengan] Активация аккаунта Муррена'
            html_data = render_to_string('activation_email.html', {'uri': message, 'murren_name': user.username})
            send_mail(subject, None, 'Murrengan <murrengan.test@gmail.com>',
                      [murren_data.get('email')], html_message=html_data)

            return JsonResponse({'is_murren_created': 'true'})

        else:

            return JsonResponse(form.errors)


def murren_activate(request):
    if request.method == 'POST':

        try:

            json_data = json.loads(request.body)
            murren_email = force_text(urlsafe_base64_decode(json_data['murren_email']))
            murren = Murren.objects.get(email=murren_email)

        except(TypeError, ValueError, OverflowError, Murren.DoesNotExist) as error:

            murren = None

        if murren is not None:

            murren.is_active = True
            murren.save()

            return JsonResponse({'murren_is_active': True})

        else:

            return JsonResponse({'error_on_backend': True, 'error_text': error.args[0]})


@require_POST
def reset_password(request):
    if not request.body:
        return JsonResponse({
            'ok': False, 'message': 'Тело запроса пустое'
        })

    data = json.loads(request.body)
    
    if 'email' not in data or not data['email']:
        return JsonResponse({
            'ok': False, 'message': 'Почта нужна для восстановления пароля'
        })
    
    try:
        murren = Murren.objects.get(email=data['email'])
    except Murren.DoesNotExist:
        return JsonResponse({
            'ok': False, 'message': 'Такой почты нет в системе'
        })

    if not murren.is_active:
        return JsonResponse({
            'ok': True, 'message': 'Вы получите письмо с востановлением данных на эту почту, '
                                   'если она была подтверждена'
        })

    # Generate token
    token = create_token_reset_password()
    password_reset = PasswordReset.objects.create_token(murren, murren.password, token)
    
    uri = f'{base_url}/set_new_password/{password_reset.token}'
    subject = '[murrengan] Восстановление пароля'
    html_message = render_to_string('reset_email.html', {
        'uri': uri, 'murren_name': password_reset.murren.username
    })
    send_mail(subject, None, 'Murrengan <murrengan.test@gmail.com>',
              [murren.email], html_message=html_message)

    return JsonResponse({
        'ok': True, 'message': 'Вы получите письмо с востановлением данных на эту почту, '
                               'если она была подтверждена'
    })


@require_POST
def confirm_new_password(request):
    if not request.body:
        return JsonResponse({
            'ok': False, 'message': 'Тело запроса пустое'
        })

    data = json.loads(request.body)

    if 'token' not in data or not data['token']:
        return JsonResponse({
            'ok': False, 'message': 'Ваш запрос без токена'
        })

    if 'password' not in data or not data['password']:
        return JsonResponse({
            'ok': False, 'message': 'Вы не указали пароль'
        })

    try:
        password = PasswordReset.objects.get(token=data['token'])
    except PasswordReset.DoesNotExist:
        return JsonResponse({
            'ok': False, 'message': 'Ошибка токена'
        })

    if password.is_password_changed():
        return JsonResponse({
            'ok': False, 'message': 'Вы уже поменяли пароль'
        })

    is_last_password_match = PasswordReset.objects.is_last_password_match(password.murren,
                                                                          raw_password=data['password'],
                                                                          replay=settings.MURREN_PASSWORD_REPLAY)
    if is_last_password_match:
        return JsonResponse({
            'ok': False, 'message': 'Ваш новый пороль не должен совпадать с вашими старыми'
        })

    password.set_password(data['password'])

    return JsonResponse({
        'ok': True, 'message': 'Пароль успешно изменен. Добро пожаловать 😎'
    })
