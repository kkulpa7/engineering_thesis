from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth import password_validation

from .models import Profile, Message

from django.utils.safestring import mark_safe

class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Hasło",
        strip=False,
        widget=forms.PasswordInput,
        # help_text=password_validation.password_validators_help_text_html(),
        # help_text=mark_safe("<ul>" +
        #     "<li>Your password can’t be too similar to your other personal information.</li>" +
        #     "<li>Your password must contain at least 8 characters.</li>" +
        #     "<li>Your password can’t be a commonly used password.</li>" +
        #     "<li>Your password can’t be entirely numeric.</li>" +
        #     "</ul>"),
        help_text=mark_safe("<ul>" +
            "<li>Twoje hasło nie może być za bardzo podobne do innych osobistych danych.</li>" +
            "<li>Twoje hasło musi zawierać co najmniej 8 znaków.</li>" +
            "<li>Twoje hasło nie może być powszechnie używanym hasłam.</li>" +
            "<li>Twoje hasło nie może składać się tylko z cyfr.</li>" +
            "</ul>"),
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

        for field in self.fields.values():
            field.required = True


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
        help_text=mark_safe("<ul>" +
            "<li>Twoje hasło nie może być za bardzo podobne do innych osobistych danych.</li>" +
            "<li>Twoje hasło musi zawierać co najmniej 8 znaków.</li>" +
            "<li>Twoje hasło nie może być powszechnie używanym hasłam.</li>" +
            "<li>Twoje hasło nie może składać się tylko z cyfr.</li>" +
            "</ul>"),
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
            'bio',
            'email',
            'branch',
            'street',
            'zip_code',
            'city',
            'profile_image'
        ]
        labels = {
            'username': 'Login',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
            'branch': 'Oddział',
            'street': 'Ulica/Miejscowość',
            'zip_code': 'Kod pocztowy',
            'city': 'Poczta',
            'profile_image': 'Zdjęcie profilowe',
            'bio': 'Opis'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name.find('image') != -1:
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
                field.widget.attrs.update({'placeholder': field.label})

        required_fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'profile_image'
        ]

        for field in required_fields:
            self.fields[field].required = True


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
