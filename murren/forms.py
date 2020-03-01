from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

Murren = get_user_model()


class MurrenSignupForm(ModelForm):

    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:

        model = Murren
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as exc:
            raise forms.ValidationError({'password': exc.messages})
