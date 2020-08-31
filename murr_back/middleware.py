import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.conf import settings
from django.db import close_old_connections
from django.http import JsonResponse
from jwt import decode as jwt_decode

from common_helpers.recaptcha import check_recaptcha

URL_PROTECTED = settings.RECAPTCHA_URL_PROTECTED


class CheckRecaptchaMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        url_is_protect = path in URL_PROTECTED

        if request.method == 'POST' and url_is_protect:
            json_data = json.loads(request.body)

            if 'recaptchaToken' in json_data:

                recaptcha_response = check_recaptcha(json_data['recaptchaToken'])
                if recaptcha_response['recaptcha_response_problem'] is True:
                    return JsonResponse({'recaptcha_response_problem': True,
                                         'recaptcha_response_text': recaptcha_response['recaptcha_response_text']},
                                        status=400)
            else:
                return JsonResponse(
                    {'recaptcha_response_problem': True,
                     'recaptcha_response_text': 'Not found recaptchaToken'},
                    status=400)

        return self.get_response(request)


class SocketTokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        database_sync_to_async(close_old_connections)()
        if scope['headers'][0][0] == 'pytest':
            return self.inner(dict(scope, user=scope['headers'][0][1]))
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        #  todo add token verification
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        pk = decoded_data["user_id"]

        return self.inner(dict(scope, user=pk))
