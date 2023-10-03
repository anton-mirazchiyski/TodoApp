from django import forms

from todo_app.accounts.models import Account


class AccountCreateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

        labels = {
            'username': 'Username',
            'password': 'Password',
            'repeated_password': 'Password'
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }),
            'repeated_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Repeat password'
            })
        }


class AccountLoginForm(AccountCreateForm):
    pass


class AccountLogoutForm(forms.Form):
    pass
