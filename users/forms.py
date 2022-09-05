from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth import password_validation

from .models import Profile, Message


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html(),
        help_text=None,
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        strip=False,
        widget=forms.PasswordInput,
        help_text=None,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Login',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email'
        }
        help_texts = {
            'username': None
        }

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})

        self.fields['username'].widget.attrs.update({'autofocus': False})


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Stare hasło",
        strip=False,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html(),
        help_text=None,
    )
    new_password1 = forms.CharField(
        label="Nowe hasło",
        strip=False,
        widget=forms.PasswordInput,
        help_text=None,
    )
    new_password2 = forms.CharField(
        label="Powtórz nowe hasło",
        strip=False,
        widget=forms.PasswordInput,
        help_text=None,
    )

    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]
        labels = {
            'username': 'Login',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'sender_2',
            'subject',
            'text'
        ]
        labels = {
            'sender_2': 'Nadawca',
            'subject': 'Temat',
            'text': 'Wiadomość'
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'placeholder': field.label})
