from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
import json

# 3rd party
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# local
from murren.serializers import MurrenSerializers, PublicMurrenInfoSerializers

# services
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


def murren_register(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        try:
            user = auth.register(json_data['email'], json_data['password'], json_data['username'])
        except(TypeError, ValueError, OverflowError) as error:
            return JsonResponse({'error_on_backend': True, 'error_text': error.args[0]})

        if not user['error']:
            token = confirm.generate_email_token(user['user'])
            confirm_result = confirm.send_confirm('reset_email.html', '[murrengan] Активация аккаунта Муррена', user['user'].email, 'Murrengan <murrengan.test@gmail.com>', token, user['user'], 'murren_email_activate')
            return JsonResponse({'is_murren_created': 'true'})
        else:
            return JsonResponse(user['error_text'])


def murren_activate(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        
        try:
            murren_code = json_data['murren_code']
        except(TypeError, ValueError, OverflowError) as error:
            return JsonResponse({'error_on_backend': True, 'error_text':error.args[0]})

        user = confirm.check_email_token(murren_code, 24, 3)

        if not user['error']:
            if auth.activate(user['user']):
                return JsonResponse({'murren_is_active': True})
        else:
            return JsonResponse({'error_on_backend': True, 'error_text': user['error_text']})    
            


def reset_password(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        try:
            user = Murren.objects.get(email=json_data['email'])
        except(TypeError, ValueError, OverflowError, Murren.DoesNotExist) as error:
            return JsonResponse({'error_on_backend': True, 'error_text':error.args[0]})

        token = confirm.generate_email_token(user)

        confirm_result = confirm.send_confirm('reset_email.html', '[murrengan] Восстановление пароля Муррена', user.email, 'Murrengan <murrengan.test@gmail.com>', token, user, 'set_new_password')

        if confirm_result:
            return JsonResponse({'email_sent_successfully': True})


def confirm_new_password(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        try:
            murren_code = json_data['murren_code']
            murren_password_1 = json_data['murren_password_1']
            murren_password_2 = json_data['murren_password_2']
        except(TypeError, ValueError, OverflowError) as error:
            return JsonResponse({'error_on_backend': True, 'error_text':error.args[0]})

        if murren_password_1 != murren_password_2:
            return JsonResponse({'password_not_equal': 'true'})

        user = confirm.check_email_token(murren_code, 24, 3)

        if not user['error']:
            if auth.reset_password(murren_password_1, user['user']):
                return JsonResponse({'password_successfully_changed': True})
        else:
             return JsonResponse({'error_on_backend': True, 'error_text': user['error_text']})
            
