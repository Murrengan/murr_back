import json
import re

from django.conf import settings
from django.http import JsonResponse

from server_settings.common import check_recaptcha

URL_PROTECTED = []
if hasattr(settings, 'RECAPTCHA_URL_PROTECTED'):
    URL_PROTECTED += [re.compile(url) for url in settings.RECAPTCHA_URL_PROTECTED]


class CheckRecaptchaMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        url_is_protect = any(url.match(path) for url in URL_PROTECTED)

        if request.method == 'POST' and url_is_protect:
            json_data = json.loads(request.body)

            if 'recaptchaToken' in json_data:

                recaptcha_response = check_recaptcha(json_data['recaptchaToken'])
                if recaptcha_response['recaptcha_response_problem'] is True:
                    return JsonResponse({'recaptcha_response_problem': True,
                                         'recaptcha_response_text': recaptcha_response['recaptcha_response_text']})
            else:
                return JsonResponse(
                    {'recaptcha_response_problem': True, 'recaptcha_response_text': 'Not found recaptchaToken'}
                )

        return self.get_response(request)
