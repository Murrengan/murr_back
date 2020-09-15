import requests

recaptcha_server_token = '6Lc0qP4UAAAAAHOoKTRWpWhfoIXSoAUh0HDaAaB4'


def check_recaptcha(token: str) -> dict:
    recaptcha = {
        'response': token,
        'secret': recaptcha_server_token
    }

    recaptcha_response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha)
    recaptcha_response_text = recaptcha_response.json()

    if recaptcha_response_text['success']:
        return {'recaptcha_response_problem': False}
    return {'recaptcha_response_problem': True, 'recaptcha_response_text': recaptcha_response_text}
