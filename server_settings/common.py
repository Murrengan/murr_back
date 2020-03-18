import json

import requests

recaptcha_server_token = '6Lesdd8UAAAAAJ4uDqjsX85z-81w87DDYsnwZjDd'
base_url = 'http://murrengan.ru'

def check_recaptcha(token):
    recaptcha = {
        'response': token,
        'secret': recaptcha_server_token
    }

    recaptcha_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha)
    recaptcha_response_text = json.loads(recaptcha_response.text)

    if recaptcha_response_text['success'] is False:
        return {'recaptcha_response_problem': True, 'recaptcha_response_text': recaptcha_response_text}
    return {'recaptcha_response_problem': False}

