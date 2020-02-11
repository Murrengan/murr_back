from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

Murren = get_user_model()


class MurrenSignupForm(ModelForm):

    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:

        model = Murren
        fields = ('username', 'email', 'password')
