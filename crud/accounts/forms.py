from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy

class CustomSignupForm(SignupForm):
    captcha = CaptchaField(label=("Verificación"))

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)


