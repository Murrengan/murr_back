from django.conf import settings as base_settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from djoser import utils
from djoser.conf import settings
from templated_mail.mail import BaseEmailMessage


class CustomEmailMessage(BaseEmailMessage):
    def send(self, *args, **kwargs):
        context = self.get_context_data()
        subject = '[murrengan] Активация аккаунта Муррена'
        html_data = render_to_string(self.template_name, context)
        # todo: Remove email not hardcode this
        send_mail(subject, None, 'Murrengan <murrengan.test@gmail.com>',
                  [context['murren_email']], html_message=html_data)


class MurrenActivationEmail(CustomEmailMessage):
    template_name = "_email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["base_url"] = base_settings.FRONTEND_URL
        context["murren_name"] = user.username
        context["murren_email"] = user.email
        return context


class MurrenPasswordResetEmail(CustomEmailMessage):
    template_name = "_email/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["base_url"] = base_settings.FRONTEND_URL
        context["murren_name"] = user.username
        context["murren_email"] = user.email
        return context
