from django import forms
from captcha.fields import CaptchaField

class VerificacionForm(forms.Form):
    nombre = forms.CharField(label="Nombre")
    email = forms.EmailField(label="Correo electrónico")
    captcha = CaptchaField()