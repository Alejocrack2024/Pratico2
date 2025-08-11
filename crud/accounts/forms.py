# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

# --- Tu formulario de verificacion (igual estilo) ---
class VerificacionForm(forms.Form):
    codigo = forms.CharField(max_length=10, label="Código")

# --- Formulario para login con captcha ---
class CaptchaAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(label='Captcha')

    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'usuario'
    }))
    password = forms.CharField(label='Contraseña', strip=False, widget=forms.PasswordInput(attrs={
        'placeholder': 'contraseña'
    }))

# --- Formulario para signup con captcha (extiende UserCreationForm) ---
class CaptchaUserCreationForm(UserCreationForm):
    captcha = CaptchaField(label='Captcha')

    email = forms.EmailField(required=True, label="Correo")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return email
