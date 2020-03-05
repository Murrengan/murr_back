from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings

import json

from django.views.decorators.http import require_POST
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from murren.serializers import MurrenSerializers, PublicMurrenInfoSerializers

import murren.services.auth as auth
import murren.services.email_confirm as confirm

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


@require_POST
def murren_register(request):
    if not request.body:
        return JsonResponse({
            'ok': False, 'message': 'Тело запроса пустое'
        })

    data = json.loads(request.body)

    user = auth.register(data)

    if not user['error']:
        return JsonResponse({
            'ok': True, 'message': 'Регистрация прошла успешно. Вы получите письмо с подтверждением'
        })
    else:
        return JsonResponse({
            'ok': False, 'message': user['error_text']
        })


@require_POST
def murren_activate(request):
    if not request.body:
        return JsonResponse({
            'ok': False, 'message': 'Тело запроса пустое'
        })

    data = json.loads(request.body)
    
    if 'email_token' not in data or not data['email_token']:
        return JsonResponse({
            'ok': False, 'message': 'Ваш запрос без токена'
        })

    user = confirm.check_email_token(data['email_token'], 
                                     'user-active', 
                                     settings.EMAIL_TOKEN_LIFETIME)
    
    if user['error'] and user['type'] == 'email_token':
        return JsonResponse({
            'ok': False, 'message': 'Ошибка токена'
        })
    
    if not user['error']:
        if auth.activate(user['user']):
            return JsonResponse({
                'ok': True, 'message': 'Активация прошла успешно. Добро пожаловать 😎'
            })
            

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
        user = Murren.objects.get(email=data['email'])
    except Murren.DoesNotExist:
        return JsonResponse({
            'ok': False, 'message': 'Такой почты нет в системе'
        })

    token = confirm.generate_email_token(user, 'reset-password', user.password)
    url = confirm.generate_confirm_url('set_new_password', token)
    confirm_result = confirm.send_confirm('activation_email.html', 
                                          '[murrengan] Восстановление пароля Муррена',
                                           settings.EMAIL_FROM, user, url)

    if confirm_result:
        return JsonResponse({
            'ok': True, 'message': 'Вы получите письмо с востановлением данных на эту почту'
        })


@require_POST
def confirm_new_password(request):
    if not request.body:
        return JsonResponse({
            'ok': False, 'message': 'Тело запроса пустое'
        })
    
    data = json.loads(request.body)

    if 'email_token' not in data or not data['email_token']:
        return JsonResponse({
            'ok': False, 'message': 'Ваш запрос без токена'
        })

    if 'password_first' not in data or not data['password_first']:
        return JsonResponse({
            'ok': False, 'message': 'Вы не указали пароль'
        })

    try:
        validate_password(data['password_first'])
    except ValidationError:
        return JsonResponse({
            'ok': False, 'message': 'Пароль является слабым'
        })

    if data['password_first'] != data['password_second']:
        return JsonResponse({
            'ok': False, 'message': 'Подтверждение не совпадает с паролем'
        })

    user = confirm.check_email_token(data['email_token'], 
                                     'reset-password', 
                                     settings.EMAIL_TOKEN_LIFETIME)

    if not user['error']:
        if auth.reset_password(data['password_second'], user['user']):
            return JsonResponse({
                'ok': True, 'message': 'Пароль успешно изменен. Добро пожаловать 😎'
            })
    else:
        return JsonResponse({
            'ok': False, 'message': 'Ошибка токена'
        })
