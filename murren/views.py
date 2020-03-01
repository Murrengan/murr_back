from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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
from server_settings.common import base_url
from .forms import MurrenSignupForm

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


def reset_password(request):
    if request.method == 'POST':

        json_data = json.loads(request.body)

        try:

            json_data = json.loads(request.body)
            email = json_data['email']
            murren = Murren.objects.get(email=email)

        except(TypeError, ValueError, OverflowError, Murren.DoesNotExist) as error_text:

            error = error_text
            murren = None

        if murren is not None:

            message = base_url + '/set_new_password/?activation_code=' \
                      + urlsafe_base64_encode(force_bytes(murren.email))
            subject = '[murrengan] Восстановление пароля Муррена'
            html_data = render_to_string('reset_email.html', {'uri': message, 'murren_name': murren.username})
            send_mail(subject, None, 'Murrengan <murrengan.test@gmail.com>', [murren.email], html_message=html_data)

            return JsonResponse({'email_sent_successfully': True})

        else:

            return JsonResponse({'error_on_backend': True, 'error_text': error.args[0]})


def confirm_new_password(request):
    if request.method == 'POST':

        json_data = json.loads(request.body)

        murren_email = force_text(urlsafe_base64_decode(json_data['murren_email']))
        murren_password_1 = json_data['murren_password_1']
        murren_password_2 = json_data['murren_password_2']

        if murren_password_1 != murren_password_2:
            return JsonResponse({'password_not_equal': 'true'})
        try:
            validate_password(murren_password_1)
        except ValidationError as exc:
            return JsonResponse({'password_not_valid': True, 'password': exc.messages})

        try:

            murren = Murren.objects.get(email=murren_email)

        except(TypeError, ValueError, OverflowError, Murren.DoesNotExist) as error_text:

            error = error_text
            murren = None

        if murren is not None:

            murren.set_password(murren_password_2)
            murren.is_active = True
            murren.save()

            return JsonResponse({'password_successfully_changed': True})

        else:

            return JsonResponse({'error_on_backend': True, 'error_text': error.args[0]})
