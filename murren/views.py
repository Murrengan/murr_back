import requests
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import json

# 3rd party
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# local
from murren.serializers import MurrenSerializers, PublicMurrenInfoSerializers
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
        qs = Murren.objects.all()
        serializer = MurrenSerializers(qs, many=True)
        return Response(serializer.data)


def murren_register(request):
    if request.method == 'POST':

        json_data = json.loads(request.body)

        recaptcha = {
            'response': json_data['recaptchaToken'],
            'secret': '6LfLNNcUAAAAAC_GSWQztiI2NVqnJbicZI53SCE9'

        }

        recaptcha_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha)
        recaptcha_response_text = json.loads(recaptcha_response.text)

        if (recaptcha_response_text['success'] is False) or (recaptcha_response_text['score'] < 0.5):
            return JsonResponse({'recaptcha_response_problem': True,
                                 'recaptcha_response_text': recaptcha_response_text})

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

            message = 'http://127.0.0.1:8080' + '/murren_email_activate/?activation_code=' \
                      + urlsafe_base64_encode(force_bytes(user.pk))
            subject = 'Активация аккаунта Муррена'
            email = EmailMessage(subject, message, to=[murren_data.get('email')])
            email.send()

            return JsonResponse({'is_murren_created': 'true'})

        else:

            return JsonResponse(form.errors)


def murren_activate(request):
    if request.method == 'POST':

        try:

            json_data = json.loads(request.body)
            murren_id = force_text(urlsafe_base64_decode(json_data['murren_id']))
            murren = Murren.objects.get(pk=murren_id)

        except(TypeError, ValueError, OverflowError, Murren.DoesNotExist) as error:

            murren = None

        if murren is not None:

            murren.is_active = True
            murren.save()

            return HttpResponse("User is active now")

        else:

            return HttpResponse('Activation link is invalid!')
