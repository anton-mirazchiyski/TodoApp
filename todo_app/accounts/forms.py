from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from utils.accounts_utils import set_placeholder

UserModel = get_user_model()


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            set_placeholder(field, self.fields)

    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Repeat Password'
        }


class AccountLoginForm(RegistrationForm):
    pass


class AccountLogoutForm(forms.Form):
    pass
