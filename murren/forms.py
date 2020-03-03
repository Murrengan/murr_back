from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

Murren = get_user_model()


class MurrenSignupForm(ModelForm):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(max_length=150, required=True)
    username = forms.CharField(max_length=24, required=True)

    class Meta:
        model = Murren
        fields = ('username', 'email', 'password', 'is_active')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as exc:
            raise forms.ValidationError({'password': exc.messages})

        cleaned_data['is_active'] = False
        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password')

        if password:
            user.set_password(raw_password=password)

        if commit:
            user.save()

        return user
