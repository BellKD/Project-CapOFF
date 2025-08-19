from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2")

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Имя"}),
            "last_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Фамилия"}),
            "password1": forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Пароль"}),
            "password2": forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Повторите пароль"}),
        }
